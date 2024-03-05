"use strict";

const $cupcakeForm = $("#add-cupcake-form");
const $cupcakeList = $("#cupcake-list");
const $submitButton = $("#submit-cupcake-btn");


/**
 grabs form data from our cupcake form, returns object with form data
 */
function getFormData() {


  let flavor = $('#flavor').val();
  let size = $('#size').val();
  let rating = $('#rating').val();
  let image_url = $('#image_url').val();
  console.log("requestBody is =", { flavor, size, rating, image_url });

  return { flavor, size, rating, image_url };

}

/**
 *
 * fetches post request to our api, returns response data
 */

async function getCupcakeResponse() {
  const requestBody = getFormData();
  console.log("this is the requestBody=", requestBody);
  const response = await fetch(
    '/api/cupcakes',
    {
      method: "POST",
      body: JSON.stringify(requestBody),
      headers: { "content-type": "application/json" },
    });

  const data = await response.json();

  return data["cupcake"];
};

/**
 * adds existing cupcakes to the top of form
 */

function appendListElements(data) {

  const flavor = data.flavor;
  const $li = $('<li>').text(flavor);
  const $img = $('<img>').attr({ "src": data.image_url, 'width': "200px", 'height': "200px" });
  $cupcakeList.append($img, $li);


}

/**
 * handles form submit, displays data above
 */

async function handleFormSubmit(evt) {
  evt.preventDefault();

  const data = await getCupcakeResponse();

  appendListElements(data);

}

$cupcakeForm.on('submit', handleFormSubmit);

