genRandomNumbers = function getRandomNumbers() {
  const array = new Uint32Array(10);
  crypto.getRandomValues(array);

  const randText = document.getElementById("myRandText");
  randText.textContent = "The random numbers are: "
  for (let i = 0; i < array.length; i++) {
    randText.textContent += array[i] + " ";
  }
}