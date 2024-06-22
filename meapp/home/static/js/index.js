var request_array = {};
var windows = [];
var walls = [];
var equipments = {};
var occupants = 0;
var roof = {};
var total = {};

async function CHGWalls() {
  walls = [];
  for (let i = 1; i < 5; i++) {
    const thermal_conductivity = parseFloat(
      document.getElementById(`k-wall-${i}`).value
    );
    const thickness = parseFloat(document.getElementById(`d-wall-${i}`).value);
    const height = parseFloat(
      document.getElementById(`height-wall-${i}`).value
    );
    const width = parseFloat(document.getElementById(`width-wall-${i}`).value);
    const temperature = parseFloat(
      document.getElementById(`temperature-wall-${i}`).value
    );
    const wallheat = {
      thermal_conductivity,
      thickness,
      height,
      width,
      temperature,
    };
    walls.push(wallheat);
  }
  console.log(walls);

  total.walls = await getheatload({ walls });
  document.getElementById(
    "result-wall"
  ).innerText = `Total Heat Gain Through Roof: ${total.walls?.total_heat_load}`;
}

async function CHGWindows() {
  const thermal_conductivity = parseFloat(
    document.getElementById("k-window").value
  );
  const thickness = parseFloat(document.getElementById("d-window").value);
  const area = parseFloat(document.getElementById("area-window").value);
  const temperature = parseFloat(
    document.getElementById("temperature-window").value
  );

  const windowheat = { thermal_conductivity, thickness, area, temperature };
  windows.push(windowheat);
  console.log(windows);
  total.windows = await getheatload({windows})
  document.getElementById('result-window').innerText = `Total Heat Gain Through Roof: ${total.windows?.total_heat_load}`;
}

async function CHGRoofs() {
  const thermal_conductivity = parseFloat(
    document.getElementById("k-roof").value
  );
  const thickness = parseFloat(document.getElementById("d-roof").value);
  const area = parseFloat(document.getElementById("area-roof").value);
  const temperature = parseFloat(
    document.getElementById("temperature-roof").value
  );

  roof = { thermal_conductivity, thickness, area, temperature };
  console.log(roof);

  total.roof = await getheatload({ roof });
  document.getElementById(
    "result-roof"
  ).innerText = `Total Heat Gain Through Roof: ${total.roof?.total_heat_load}`;
}

async function CHGOccupants() {
  const occupants = parseInt(document.getElementById("occupants").value);

  console.log(occupants);
  total.occupants = await getheatload({ occupants });
  document.getElementById(
    "result-occupant"
  ).innerText = `Total Heat Gain Through Roof: ${total.occupants?.total_heat_load}`;
}

async function CHGEquipments() {
  const computer = parseFloat(
    document.getElementById("computer-equipment").value
  );
  const fans = parseFloat(document.getElementById("fan-equipment").value);
  const led_tubelight = parseFloat(
    document.getElementById("ledtubelight-equipment").value
  );

  equipments = { computer, fans, led_tubelight };
  console.log(equipments);

  total.equipments = await getheatload({ equipments });
  document.getElementById(
    "result-equipment"
  ).innerText = `Total Heat Gain Through Roof: ${total.equipments?.total_heat_load}`;
}

async function CHGTotal() {
  document.getElementById("walls-total").value = total.walls.total_heat_load || ''
  document.getElementById("window-total").value = total.windows.total_heat_load || ''
  document.getElementById("roof-total").value = total.roof.total_heat_load || ''
  document.getElementById("occupants-total").value = total.occupants.total_heat_load || ''
  document.getElementById("computers-total").value = total.equipments.total_heat_load || ''
  document.getElementById("lights-total").value = total.equipments.total_heat_load || ''
  document.getElementById("fans-total").value = total.equipments.total_heat_load || ''
  
  request_array = { walls, windows, roof, occupants, equipments };
  console.log(request_array);
  total.total = await getheatload({total})

  document.getElementById("result").innerHTML = `
        <p>Total Heat Gain: ${total.total?.total_heat_load}</p>
        <p>Tonnage Required: ${total.total?.air_conditioning}</p>
    `;
}

async function getheatload(json_data = {}) {
  try {
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(json_data),
    };
    const response = await fetch(
      "http://127.0.0.1:8000/api/calculation/",
      options
    );
    const movies = await response.json();
    return movies.data;
  } catch (e) {
    console.log(e.message);
    return e.message;
  }
}

// Simulated user information (replace with actual user data handling)
const user = {
  name: "John Doe",
  email: "john.doe@example.com",
  role: "User",
};

// Display user information
document.getElementById("userInfo").innerHTML = `
    <p><strong>Name:</strong> ${user.name}</p>
    <p><strong>Email:</strong> ${user.email}</p>
    <p><strong>Role:</strong> ${user.role}</p>
`;
