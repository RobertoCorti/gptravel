document.addEventListener('DOMContentLoaded', () => {
  const fromDropdown = document.querySelector('#from');
  const toDropdown = document.querySelector('#to');
  const departureDateInput = document.getElementById("departure-date");
  const returnDateInput = document.getElementById("return-date");

  fetch('https://restcountries.com/v3.1/all')
    .then(res => res.json())
    .then(data => {
      const sortedData = data.sort((a, b) => a.name.common.localeCompare(b.name.common));
      let countryOutput = "<option disabled selected value>Select a Country</option>";
      sortedData.forEach(country => {
        countryOutput += `
          <option value="${country.altSpellings[0]}">${country.name.common}</option>
        `;
      })
      fromDropdown.innerHTML = countryOutput;
      toDropdown.innerHTML = countryOutput;
    })
    .catch(err => console.error(err));

  // Check if departure date is before return date
  returnDateInput.addEventListener('change', event => {
    // check if value is not empty
    if (returnDateInput.value !== '' && departureDateInput.value !== '') {
        if (departureDateInput.value > returnDateInput.value) {
            alert('Return date must be after departure date');
            returnDateInput.value = departureDateInput.value;
        }
    }
  });

});

/*
// Define the API endpoint
const endpoint = 'https://restcountries.com/v3.1/all';

function fetchCountryNames() {
  return fetch("https://restcountries.com/v3.1/all")
    .then(response => response.json())
    .then(data => data.map(country => country.name.common))
    .catch(error => {
      console.error(error);
      return [];
    });
}
let countries = [];
fetchCountryNames().then(data => {
      countries = data;
});

const resultBox = document.querySelector('.result-box');
const inputBoxFrom = document.getElementById('from');

inputBoxFrom.onkeyup = function(){
    let result = [];
    let input = inputBoxFrom.value;
    if(input.length){
        result = countries.filter((country)=>{
            return country.toLowerCase().includes(input.toLowerCase());
        });
        console.log(result);
    }
    display(result);

    if (!result.length){
        resultBox.innerHTML = '';
    }
}

function display(result){
    const content = result.map((list) => {
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });

    resultBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
    inputBoxFrom.value = list.innerHTML;
    resultBox.innerHTML = '';
}
*/
/*document.addEventListener('DOMContentLoaded', () => {
  const countryDropdown = document.querySelector('#country');
  const regionDropdown = document.querySelector('#region');
  const departureDateInput = document.getElementById("departure_date");
  const returnDateInput = document.getElementById("return_date");


  fetch('https://restcountries.com/v3.1/all')
    .then(res => res.json())
    .then(data => {
      const sortedData = data.sort((a, b) => a.name.common.localeCompare(b.name.common));
      let countryOutput = "<option disabled selected value>Select a Country</option>";
      sortedData.forEach(country => {
        countryOutput += `
          <option value="${country.altSpellings[0]}">${country.name.common}</option>
        `;
      })
      countryDropdown.innerHTML = countryOutput;
    })
    .catch(err => console.error(err));

  countryDropdown.addEventListener('change', () => {
    const selectedCountryCode = countryDropdown.value;
    if (selectedCountryCode !== '') {
      fetch(`http://api.geonames.org/searchJSON?country=${selectedCountryCode}&featureCode=ADM1&username=robcorti`)
        .then(res => res.json())
          .then(data => {
            const regions = data.geonames.sort((a, b) => a.name.localeCompare(b.name));
            let regionOutput = "<option disabled selected value>Select a Region</option>";
            regions.forEach(region => {
              regionOutput += `
               <option value="${region.name}">${region.name}</option>
            `;
          })
          regionDropdown.innerHTML = regionOutput;
        })
        .catch(err => console.error(err));
    } else {
      regionDropdown.innerHTML = "<option disabled selected value>Select a Region</option>";
    }
  });
  // Check if departure date is before return date
  returnDateInput.addEventListener('change', event => {
    // check if value is not empty
    if (returnDateInput.value !== '' && departureDateInput.value !== '') {
        if (departureDateInput.value > returnDateInput.value) {
            alert('Return date must be after departure date');
            returnDateInput.value = departureDateInput.value;
        }
    }
  });
});
*/
