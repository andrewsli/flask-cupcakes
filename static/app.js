const BASE_URL = "http://localhost:5000";
$(async function() {

  async function generate_html(){
    response = await axios.get(BASE_URL + '/cupcakes')
    cupcakes = response.data["response"]
    for(let cupcake of cupcakes){
      $("#cupcakes_container").append(generate_cupcake_html(cupcake))
    }
    return;
  }


  function generate_cupcake_html(cupcake){
    return `<div class="cupcake mr-3">
        <img src="${cupcake.image}"></img>
        <p>Flavor: ${cupcake.flavor}<br> Size: ${cupcake.size}<br> Rating: ${cupcake.rating}<br></p>
    </div>`
  }

  $("#button").on("click", function(evt) {
    evt.preventDefault();
    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image_url = $("#image").val();

    $("#cupcakes_container").append(
      `<div class="cupcake mr-3">
        <img src="${image_url}"></img>
        <p>Flavor: ${flavor}<br> Size: ${size}<br> Rating: ${rating}<br></p>
    </div>`
    )

    $("#add_cupcake_form").trigger("reset");
  });

  generate_html();
});
