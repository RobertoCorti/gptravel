document.addEventListener('DOMContentLoaded', () => {
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

