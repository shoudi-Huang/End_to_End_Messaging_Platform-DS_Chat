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

async function generateKeyPair() {
  return await crypto.subtle.generateKey(
    {
      name: "RSA-PSS",
      modulusLength: 2048, //密钥长度，可以是1024, 2048, 4096，建议2048以上
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]), // 公共指数e，一般用65537
      hash: "SHA-256", //可以是"SHA-1", "SHA-256", "SHA-384", "SHA-512"
    },
    true,
    ["sign", "verify"]
  );
}

const keyPair = await generateKeyPair();
const signature = await signMessage(text, keyPair.privateKey);
const result = await verifyMessage(text, signature, keyPair.publicKey);
console.log(result); // true



async function testing1(Id) {
    const text = document.getElementById(Id).textContent;
    console.log(text)

    const publicKey = await importPublicKey(pubk_pemExported)
    const privateKey = await importPrivateKey(prik_pemExported)
    console.log(publicKey)
    console.log(privateKey)

    const cipherText = await encryptMessage(text, publicKey);
    const ct_exportedAsString = String.fromCharCode.apply(null, new Uint8Array(cipherText));
    const ct_exportedAsBase64 = window.btoa(ct_exportedAsString);
    const ct_pemExported = `-----BEGIN Cipher Text-----\n${ct_exportedAsBase64}\n-----END Cipher Text-----`;
    console.log(ct_pemExported)

    const plainText = await decryptMessage(cipherText, privateKey);
    console.log(plainText); // An obscure body in the S-K System, your majesty. The inhabitants refer to it as the planet Earth.
}

