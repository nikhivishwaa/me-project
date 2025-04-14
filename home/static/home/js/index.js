var request_array = {};
var windows = [];
var walls = [];
var equipments = {};
var occupants = 0;
var roof = {};
var total = {};
var conductivity = {
  brick: 0.3,
  glass: 1.0,
  wooden: 0.15,
  plywood: 0.11,
};

function getConductivity(param) {
  let value = document.querySelector(`input[name='${param}-k']:checked`).value;
  try {
    return conductivity[value];
  } catch (e) {
    console.error(e);
    return 0;
  }
}

async function CHGWalls() {
  const all_filled = validateWallForm("wall");
  if (!all_filled) {
    walls = [];
    for (let i = 1; i < 5; i++) {
      const temperature = parseFloat(
        document.getElementById(`temperature-wall-${i}`).value
      );

      const fields = getTogglerFields(`wall-${i}`);
      const thermal_conductivity =
        getConductivity(`wall-${i}`) || conductivity["brick"];
      const wallheat = { thermal_conductivity, temperature, ...fields };
      walls.push(wallheat);
    }
    console.log(walls);

    response = await getheatload({ walls });
    if (response.success) {
      total.walls = response.data;
      document.getElementById(
        "result-wall"
      ).innerText = `Total Heat Gain Through Wall: ${total.walls?.total_heat_load}`;
      changeBtnStatus(0, "success");
    } else {
      changeBtnStatus(0, "error");
    }
  }
}
async function CHGWindows() {
  const all_filled = validateTogglerForm("window");
  if (!all_filled) {
    const temperature = parseFloat(
      document.getElementById("temperature-window").value
    );

    const fields = getTogglerFields("window");
    const thermal_conductivity =
      getConductivity("window") || conductivity["glass"];
    const windowheat = { thermal_conductivity, temperature, ...fields };
    windows[0] = windowheat;
    console.log(windows);
    response = await getheatload({ windows });
    if (response.success) {
      total.windows = response.data;
      console.log(total);
      document.getElementById(
        "result-window"
      ).innerText = `Total Heat Gain Through Roof: ${total.windows?.total_heat_load}`;
      changeBtnStatus(1, "success");
    } else {
      changeBtnStatus(1, "error");
    }
  }
}
async function CHGRoof() {
  const all_filled = validateTogglerForm("roof");
  if (!all_filled) {
    const thickness = parseFloat(document.getElementById("d-roof").value);
    const temperature = parseFloat(
      document.getElementById("temperature-roof").value
    );

    const fields = getTogglerFields("roof", true);
    roof = { thickness, temperature, ...fields };
    console.log(roof);

    response = await getheatload({ roof });
    if (response.success) {
      total.roof = response.data;
      changeBtnStatus(2, "success");
      document.getElementById(
        "result-roof"
      ).innerText = `Total Heat Gain Through Roof: ${total.roof?.total_heat_load}`;
    } else {
      changeBtnStatus(2, "error");
    }
  }
}
async function CHGOccupants() {
  const all_filled = validateForm("occupant");
  if (!all_filled) {
    const occupants = parseInt(document.getElementById("occupants").value);

    console.log(occupants);
    response = await getheatload({ occupants });
    if (response.success) {
      total.occupants = response.data;
      document.getElementById(
        "result-occupant"
      ).innerText = `Total Heat Gain Through Roof: ${total.occupants?.total_heat_load}`;
      changeBtnStatus(3, "success");
    } else {
      changeBtnStatus(3, "error");
    }
  }
}

async function CHGEquipments() {
  const all_filled = validateForm("equipment");
  if (!all_filled) {
    const computer = parseFloat(
      document.getElementById("computer-equipment").value
    );
    const fans = parseFloat(document.getElementById("fan-equipment").value);
    const led_tubelight = parseFloat(
      document.getElementById("ledtubelight-equipment").value
    );

    equipments = { computer, fans, led_tubelight };
    console.log(equipments);

    response = await getheatload({ equipments });
    if (response.success) {
      total.equipments = response.data;
      changeBtnStatus(4, "success");
      document.getElementById(
        "result-equipment"
      ).innerText = `Total Heat Gain Through Roof: ${total.equipments?.total_heat_load}`;
    } else {
      changeBtnStatus(4, "error");
    }
  }
}

async function CHGTotal() {
  document.getElementById("walls-total").value =
    total.walls?.total_heat_load || "0 W";
  document.getElementById("window-total").value =
    total.windows?.total_heat_load || "0 W";
  document.getElementById("roof-total").value =
    total.roof?.total_heat_load || "0 W";
  document.getElementById("occupants-total").value =
    total.occupants?.total_heat_load || "0 W";
  document.getElementById("computers-total").value =
    total.equipments?.detailed_heat_load?.equipments
      ?.heat_gain_by_each_equipment?.computer || "0 W";
  document.getElementById("lights-total").value =
    total.equipments?.detailed_heat_load?.equipments
      ?.heat_gain_by_each_equipment?.led_tubelight || "0 W";
  document.getElementById("fans-total").value =
    total.equipments?.detailed_heat_load?.equipments
      ?.heat_gain_by_each_equipment?.fans || "0 W";

  request_array = { walls, windows, roof, occupants, equipments };
  console.log(request_array);
  response = await getheatload(request_array);
  let claculated = 0;
  document
    .querySelectorAll('#CHGTotal input[type="text"]')
    .forEach((a) => (a.value !== "0 W" ? claculated++ : ""));

  if (claculated) {
    if (response.success) {
      total.total = response.data;
      console.log(total);
      TotalTonnageAlert(
        "success",
        `You have Required : ${total?.total?.air_conditioning} AC<br><p style="color:grey; font-size: 14px; font-weight: 300;">* 1 % Infilteration added in Total.</p>`
      );
      changeBtnStatus(5, "success");
      document.getElementById("result").innerHTML = `
          <p>Total Heat Gain: ${total.total.total_heat_load}</p>
          <p>Tonnage Required: ${total.total.air_conditioning}</p>
          <p style="color:grey; font-size: 14px; font-weight: 300;">* 1 % Infilteration added in Total.</p>
      `;
    } else {
      changeBtnStatus(5, "error");
    }
  } else {
    changeBtnStatus(5, "error");
    TotalTonnageAlert(
      "warning",
      `You must Calculate any of Parameter to get Total Result`
    );
  }
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
    const response = await fetch("/api/calculation/", options);
    const movies = await response.json();
    console.log(movies);
    return movies;
  } catch (e) {
    console.log(e.message);
    return e.message;
  }
}

async function TotalTonnageAlert(type, message, secs = 15) {
  const alert = `<div class="alert alert-${
    type === "error" ? "danger" : type
  } alert-dismissible fade show w-100 py-[10px] px-[25px] absolute" role="alert">
<strong>${type[0].toUpperCase()}${type.slice(1)} : </strong >${message}
<button type="button" class="close float-right" data-dismiss="alert" aria-label="Close" onclick="this.parentNode.remove(true)">
  <span aria-hidden="true" class="text-[30px]">&times;</span>
</button>
</div >`;
  const alerts = document.getElementById("alert-area");
  alerts.innerHTML = alert;
  const dismiss_alert = alerts.lastChild;
  // setTimeout(() => dismiss_alert.remove(true), secs * 1000);
}
