document.addEventListener('DOMContentLoaded', () => {

  const selectDrop = document.querySelector('#country');
  // const selectDrop = document.getElementById('countries');


  fetch('https://restcountries.com/v3.1/all').then(res => {
    return res.json();
  }).then(data => {
    let output = "<option disabled selected value>Select a Country </option>";
    data.forEach(country => {
      output += `
      
      <option value="${country.altSpellings[0]}">${country.name.common}</option>`;
    })
    selectDrop.innerHTML = output;
  }).catch(err => {
    console.log(err);
  })


});