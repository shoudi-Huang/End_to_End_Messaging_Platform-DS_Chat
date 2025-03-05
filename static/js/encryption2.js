async function encryptMessage(message, key){
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const iv = await crypto.getRandomValues(new Uint8Array(12));
  const iv_exportedAsString = String.fromCharCode.apply(null, iv);
  const iv_pemExported = window.btoa(iv_exportedAsString);
  const cipherText = await crypto.subtle.encrypt(
    {
      name: "AES-GCM",
      iv: iv
    },
    key,
    data
  );
  //console.log(message)
  const ct_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(cipherText));
  const ct_pemExported = window.btoa(ct_exportedAsString);
  return {ct_pemExported, iv_pemExported}
}

async function decryptMessage(cipherText, key, iv){
  result = await window.crypto.subtle.decrypt(
    {
      name: "AES-GCM",
      iv: iv
    },
    key,
    cipherText
  );
  const decoder = new TextDecoder();
  return decoder.decode(result);
}

async function generateKeyPair() {
    return await crypto.subtle.generateKey(
        {
        name: "ECDH",
        namedCurve: "P-256"
        },
        true,
        ["deriveKey", "deriveBits"]
    );
}

async function deriveSecretKey(privateKey, publicKey) {
  return crypto.subtle.deriveKey(
    {
      name: "ECDH",
      public: publicKey
    },
    privateKey,
    {
      name: "AES-GCM",
      length: 256
    },
    false,
    ["encrypt", "decrypt"]
  );
}

async function generateKey(username) {
    const keyPair = await generateKeyPair();

    const pubk_exported = await crypto.subtle.exportKey(
        "spki",
        keyPair.publicKey
    );
    const pubk_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(pubk_exported));
    const pubk_exportedAsBase64 = window.btoa(pubk_exportedAsString);
    const pubk_pemExported = `-----BEGIN PUBLIC KEY-----new_line${pubk_exportedAsBase64}new_line-----END PUBLIC KEY-----`;
    //document.getElementById("publicKey").textContent = pubk_pemExported
    document.cookie = `${username}_publicKey= ; expires = Thu, 01 Jan 1970 00:00:00 GMT`
    document.cookie = `${username}_publicKey=${pubk_pemExported}`;
    console.log(pubk_pemExported)
    //pubk_pemExported = `-----BEGIN PUBLIC KEY-----\n${pubk_exportedAsBase64}\n-----END PUBLIC KEY-----`;

    const prik_exported = await window.crypto.subtle.exportKey(
        "pkcs8",
        keyPair.privateKey
    );
    const prik_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(prik_exported));
    const prik_exportedAsBase64 = window.btoa(prik_exportedAsString);
    prik_pemExported = `-----BEGIN PRIVATE KEY-----\n${prik_exportedAsBase64}\n-----END PRIVATE KEY-----`;
    localStorage.setItem(`${username}_private_key`, prik_pemExported);
    console.log(prik_pemExported)
}

function str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
      bufView[i] = str.charCodeAt(i);
    }
    return buf;
}

function importPublicKey(pem) {
    // fetch the part of the PEM string between header and footer
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pemContents);
    // convert from a binary string to an ArrayBuffer
    const binaryDer = str2ab(binaryDerString);

    return crypto.subtle.importKey(
       "spki",
       binaryDer,
       {
         name: "ECDH",
         namedCurve: "P-256",
       },
       true,
       []
     );
}

function importPrivateKey(pem) {
    // fetch the part of the PEM string between header and footer
    const pemHeader = "-----BEGIN PRIVATE KEY-----";
    const pemFooter = "-----END PRIVATE KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pemContents);
    // convert from a binary string to an ArrayBuffer
    const binaryDer = str2ab(binaryDerString);

    return  crypto.subtle.importKey(
        "pkcs8",
        binaryDer,
        {
         name: "ECDH",
         namedCurve: "P-256",
        },
        true,
        ["deriveKey", "deriveBits"]
    );
}

function importIV(pem) {
    // fetch the part of the PEM string between header and footer
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pem);
    // convert from a binary string to an ArrayBuffer
    return new Uint8Array(str2ab(binaryDerString));
}

function importCT(pem) {
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pem);
    // convert from a binary string to an ArrayBuffer
    return new Uint8Array(str2ab(binaryDerString));
}


async function testing2(Id) {
    const text = document.getElementById(Id).textContent;
    console.log(text)

    const publicKey = await importPublicKey(pubk_pemExported)
    const privateKey = await importPrivateKey(prik_pemExported)
    console.log(publicKey)
    console.log(privateKey)
    const key1 = await deriveSecretKey(privateKey, publicKey)


    const cipherTextAndIV = await encryptMessage(text, key1);
    const ct_pemExported = cipherTextAndIV.ct_pemExported
    const iv_pemExported = cipherTextAndIV.iv_pemExported
    console.log(ct_pemExported)
    console.log(iv_pemExported)

    //document.getElementById("cipherText").textContent = ct_pemExported
    //console.log(ct_pemExported)

    const publicKey2 = await importPublicKey(pubk_pemExported)
    const privateKey2 = await importPrivateKey(prik_pemExported)
    const key2 = await deriveSecretKey(privateKey2, publicKey2)
    const iv = importIV(iv_pemExported)
    const cipherText = importCT(ct_pemExported)
    const plainText = await decryptMessage(cipherText, key2, iv);
    console.log(plainText); // An obscure body in the S-K System, your majesty. The inhabitants refer to it as the planet Earth.
}

async function signMessage(message, privateKey){
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const signature = await crypto.subtle.sign(
      {
        name: "RSA-PSS",
        saltLength: 32,
      },
      privateKey,
      data
    );
  const si_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(signature));
  const si_exportedAsBase64 = window.btoa(si_exportedAsString);
  return si_exportedAsBase64
}

async function verifyMessage(message, signature, publicKey){
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  return await crypto.subtle.verify(
    {
      name: "RSA-PSS",
      saltLength: 32,
    },
    publicKey,
    signature,
    data
  );
}

async function generateSignatureKeyPair(username) {
    const signature_keyPair = await crypto.subtle.generateKey(
    {
      name: "RSA-PSS",
      modulusLength: 2048, //密钥长度，可以是1024, 2048, 4096，建议2048以上
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 公共指数e，一般用65537
      hash: "SHA-256", //可以是"SHA-1", "SHA-256", "SHA-384", "SHA-512"
    },
    true,
    ["sign", "verify"]
    );

    const pubk_exported = await crypto.subtle.exportKey(
        "spki",
        signature_keyPair.publicKey
    );

    const pubk_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(pubk_exported));
    const pubk_exportedAsBase64 = window.btoa(pubk_exportedAsString);
    signature_pubk_pemExported = `-----BEGIN PUBLIC KEY-----new_line${pubk_exportedAsBase64}new_line-----END PUBLIC KEY-----`;
    //document.getElementById("signaturePublicKey").textContent = signature_pubk_pemExported
    document.cookie = `${username}_signaturePublicKey= ; expires = Thu, 01 Jan 1970 00:00:00 GMT`
    document.cookie = `${username}_signaturePublicKey=${signature_pubk_pemExported}`;
    console.log(signature_pubk_pemExported)

    const prik_exported = await window.crypto.subtle.exportKey(
        "pkcs8",
        signature_keyPair.privateKey
    );
    const prik_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(prik_exported));
    const prik_exportedAsBase64 = window.btoa(prik_exportedAsString);
    signature_prik_pemExported = `-----BEGIN PRIVATE KEY-----\n${prik_exportedAsBase64}\n-----END PRIVATE KEY-----`;
    localStorage.setItem(`${username}_signature_private_key`, signature_prik_pemExported);
    console.log(signature_prik_pemExported)
}

function importSignaturePublicKey(pem) {
    // fetch the part of the PEM string between header and footer
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pemContents);
    // convert from a binary string to an ArrayBuffer
    const binaryDer = str2ab(binaryDerString);

    return crypto.subtle.importKey(
      "spki",
      binaryDer,
      {
        name: "RSA-PSS",
        hash: "SHA-256"
      },
      true,
      ["verify"]
    );
}

function importSignaturePrivateKey(pem) {
    // fetch the part of the PEM string between header and footer
    const pemHeader = "-----BEGIN PRIVATE KEY-----";
    const pemFooter = "-----END PRIVATE KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pemContents);
    // convert from a binary string to an ArrayBuffer
    const binaryDer = str2ab(binaryDerString);

    return crypto.subtle.importKey(
        "pkcs8",
        binaryDer,
        {
          name: "RSA-PSS",
          hash: "SHA-256",
        },
        true,
        ["sign"]
    );
}

function importSignature(pem) {
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pem);
    // convert from a binary string to an ArrayBuffer
    return new Uint8Array(str2ab(binaryDerString));
}

function cleanStorage() {
    localStorage.clear()
}

function cleanMessage(username_id) {
    const username = document.getElementById(username_id).textContent;

    document.cookie = `${username}_cipherText= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/sendMessage`
    document.cookie = `${username}_iv= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/sendMessage`
    document.cookie = `${username}_signature= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/sendMessage`

    //document.cookie = `${username}_cipherText= ; path=/sendMessage`
    //document.cookie = `${username}_iv= ; path=/sendMessage`
    //document.cookie = `${username}_signature= ; path=/sendMessage`
}

async function testing1(Id) {
    const text = cipherTextAndIV.ct_pemExported + cipherTextAndIV.iv_pemExported
    console.log(text)

    const publicKey = await importSignaturePublicKey(signature_pubk_pemExported)
    const privateKey = await importSignaturePrivateKey(signature_prik_pemExported)
    console.log(publicKey)
    console.log(privateKey)

    const si_pemExported = await signMessage(text, privateKey);

    const signature = importSignature(si_pemExported)
    const result = await verifyMessage(text, signature, publicKey);
    console.log(result); // An obscure body in the S-K System, your majesty. The inhabitants refer to it as the planet Earth.
}

async function encryption(Id, receiver_publicKey_id, username_id) {
    const plainText = document.getElementById(Id).value;
    const receiver_pubk_pemExported = document.getElementById(receiver_publicKey_id).textContent;
    const username = document.getElementById(username_id).textContent;
    //console.log(plsdsainText)
    console.log(username)

    const receiver_publicKey = await importPublicKey(receiver_pubk_pemExported)
    const prik_pemExported = localStorage.getItem(`${username}_private_key`)
    const privateKey = await importPrivateKey(prik_pemExported)

    const key = await deriveSecretKey(privateKey, receiver_publicKey)
    console.log(receiver_pubk_pemExported)
    console.log(prik_pemExported)
    console.log(key)

    const cipherTextAndIV = await encryptMessage(plainText, key);
    const ct_pemExported = cipherTextAndIV.ct_pemExported
    const iv_pemExported = cipherTextAndIV.iv_pemExported

    //document.getElementById("cipherText").textContent = ct_pemExported
    //console.log(ct_pemExported)
    const ct_iv_text = ct_pemExported + iv_pemExported
    const signature_prik_pemExported = localStorage.getItem(`${username}_signature_private_key`)
    const signature_privateKey = await importSignaturePrivateKey(signature_prik_pemExported)
    const si_pemExported = await signMessage(ct_iv_text, signature_privateKey);

    document.cookie = `${username}_cipherText= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/sendMessage`
    document.cookie = `${username}_iv= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/sendMessage`
    document.cookie = `${username}_signature= ; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/sendMessage`

    document.cookie = `${username}_cipherText=${ct_pemExported}; path=/sendMessage`
    document.cookie = `${username}_iv=${iv_pemExported}; path=/sendMessage`
    document.cookie = `${username}_signature=${si_pemExported}; path=/sendMessage`

    //const cipherText = importCT(cipherTextAndIV.ct_pemExported)
    //var arrayBuffer = cipherText.buffer.slice(cipherText.byteOffset, cipherText.byteLength + cipherText.byteOffset);
    //const iv = importIV(cipherTextAndIV.iv_pemExported)
    //const decryptText = await decryptMessage(cipherText, key, iv);
    //console.log(arrayBuffer)
    //console.log(decryptText)
}

async function decryption(plainText_id, cipherText_id, sender_publicKey_id, iv_id, signature_id, sender_signature_publicKey_id, username_id) {
    const ct_pemExported_ls = document.getElementsByName(cipherText_id);
    const plain_ls = document.getElementsByName(plainText_id);
    const sender_pubk_pemExported = document.getElementById(sender_publicKey_id).textContent;
    const iv_pemExported_ls = document.getElementsByName(iv_id);
    const si_pemExported_ls = document.getElementsByName(signature_id);
    const signature_pubk_pemExported_ls = document.getElementsByName(sender_signature_publicKey_id);
    const username = document.getElementById(username_id).textContent;
    const index = plain_ls.length-1

    const ct_pemExported = ct_pemExported_ls[ct_pemExported_ls.length-1].textContent
    const iv_pemExported = iv_pemExported_ls[iv_pemExported_ls.length-1].textContent
    const si_pemExported = si_pemExported_ls[si_pemExported_ls.length-1].textContent
    const signature_pubk_pemExported = signature_pubk_pemExported_ls[signature_pubk_pemExported_ls.length-1].textContent
    //console.log(ct_pemExported)
    //console.log(iv_pemExported)
    //console.log(si_pemExported)
    //console.log(sender_pubk_pemExported)
    //console.log()

    const cipherText = importCT(ct_pemExported)
    const sender_publicKey = await importPublicKey(sender_pubk_pemExported);
    const iv = importIV(iv_pemExported)
    const signature = importSignature(si_pemExported)
    const sender_signaturePublicKey = await importSignaturePublicKey(signature_pubk_pemExported)

    const prik_pemExported = localStorage.getItem(`${username}_private_key`)
    const privateKey = await importPrivateKey(prik_pemExported)
    //console.log(prik_pemExported)

    const ct_iv_text = ct_pemExported + iv_pemExported
    const result = await verifyMessage(ct_iv_text, signature, sender_signaturePublicKey);
    //console.log(ct_iv_text)
    //console.log(result)
    //console.log()
    if (result) {
        const key = await deriveSecretKey(privateKey, sender_publicKey)
        const plainText = await decryptMessage(cipherText, key, iv);
        //console.log(plainText)
        document.getElementsByName(plainText_id)[index].innerHTML = document.getElementsByName(plainText_id)[index].textContent + '<br/><i>' + plainText + '</i>';
        //console.log(document.getElementsByName(plainText_id))
    } else {
        console.log()
        console.log("Invalid Ciphertext")
    }
}

