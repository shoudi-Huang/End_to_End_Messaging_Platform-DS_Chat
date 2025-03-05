//const text = "An obscure body in the S-K System, your majesty. The inhabitants refer to it as the planet Earth.";

async function encryptMessage(message, publicKey){
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  return await crypto.subtle.encrypt(
      {
        name: "RSA-OAEP",
      },
      publicKey,
      data
    );
}

async function decryptMessage(cipherText, privateKey){
  const result = await crypto.subtle.decrypt(
    {
      name: "RSA-OAEP"
    },
    privateKey,
    cipherText
  );
  const decoder = new TextDecoder();
  return decoder.decode(result);
}

async function generateKeyPair() {
  return await crypto.subtle.generateKey(
    {
      name: "RSA-OAEP",
      modulusLength: 2048, //密钥长度，可以是1024, 2048, 4096，建议2048以上
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 公共指数e，一般用65537
      hash: "SHA-256", //可以是"SHA-1", "SHA-256", "SHA-384", "SHA-512"
    },
    true,
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
    pubk_pemExported = `-----BEGIN PUBLIC KEY-----new_line${pubk_exportedAsBase64}new_line-----END PUBLIC KEY-----`;
    //document.getElementById("publicKey").textContent = pubk_pemExported
    document.cookie = `${username}_publicKey=${pubk_pemExported}`;
    console.log(pubk_pemExported)

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
        name: "RSA-OAEP",
        hash: "SHA-256"
      },
      true,
      ["encrypt"]
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

    return crypto.subtle.importKey(
        "pkcs8",
        binaryDer,
        {
          name: "RSA-OAEP",
          hash: "SHA-256",
        },
        true,
        ["decrypt"]
    );
}


async function testing2(Id) {
    const text = document.getElementById(Id).textContent;
    console.log(text)

    const publicKey = await importPublicKey(pubk_pemExported)
    const privateKey = await importPrivateKey(prik_pemExported)
    console.log(publicKey)
    console.log(privateKey)

    const cipherText = await encryptMessage(text, publicKey);
    const ct_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(cipherText));
    const ct_exportedAsBase64 = window.btoa(ct_exportedAsString);
    ct_pemExported = `-----BEGIN Cipher Text-----\n${ct_exportedAsBase64}\n-----END Cipher Text-----`;
    document.getElementById("cipherText").textContent = ct_pemExported
    console.log(ct_pemExported)

    const plainText = await decryptMessage(cipherText, privateKey);
    console.log(plainText); // An obscure body in the S-K System, your majesty. The inhabitants refer to it as the planet Earth.
}

async function signMessage(message, privateKey){
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  return await crypto.subtle.sign(
      {
        name: "RSA-PSS",
        saltLength: 32,
      },
      privateKey,
      data
    );
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

async function testing1(Id) {
    const text = document.getElementById(Id).textContent;
    console.log(text)

    const publicKey = await importSignaturePublicKey(signature_pubk_pemExported)
    const privateKey = await importSignaturePrivateKey(signature_prik_pemExported)
    console.log(publicKey)
    console.log(privateKey)

    const signature = await signMessage(text, privateKey);
    const ct_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(signature));
    const ct_exportedAsBase64 = window.btoa(ct_exportedAsString);
    const ct_pemExported = `-----BEGIN Signature-----\n${ct_exportedAsBase64}\n-----END Signature-----`;
    console.log(ct_pemExported)

    const result = await verifyMessage(text, signature, publicKey);
    console.log(result); // An obscure body in the S-K System, your majesty. The inhabitants refer to it as the planet Earth.
}


