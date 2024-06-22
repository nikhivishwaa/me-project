function CHGWalls() {
    const k = parseFloat(document.getElementById('k').value);
    const d = parseFloat(document.getElementById('d').value);
    const tempDiff1 = parseFloat(document.getElementById('tempDiff1').value);
    const tempDiff2 = parseFloat(document.getElementById('tempDiff2').value);

    const area1 = 9.64 * 3.66;
    const area2 = area1; // Since Wall 1 and Wall 2 have the same area
    const area3 = 8 * 3.66;
    const area4 = area3; // Since Wall 3 and Wall 4 have the same area

    const Qwall1 = k * area1 * tempDiff1 / d;
    const Qwall2 = k * area2 * tempDiff2 / d;
    const Qwall3 = k * area3 * tempDiff2 / d;
    const Qwall4 = k * area4 * tempDiff2 / d;

    const totalHeatGain = Qwall1 + Qwall2 + 2 * Qwall3;

    document.getElementById('result').innerText = `Total Heat Gain Through Walls: ${totalHeatGain.toFixed(2)} W`;
}

function CHGWindows() {
    const k = parseFloat(document.getElementById('k').value);
    const d = parseFloat(document.getElementById('d').value);
    const area = parseFloat(document.getElementById('area').value);
    const tempDiff = parseFloat(document.getElementById('tempDiff').value);

    const Qwindow = k * area * tempDiff / d;

    document.getElementById('result').innerText = `Total Heat Gain Through Window: ${Qwindow.toFixed(2)} W`;
}


function CHGRoofs() {
    const k = parseFloat(document.getElementById('k').value);
    const d = parseFloat(document.getElementById('d').value);
    const area = parseFloat(document.getElementById('area').value);
    const tempDiff = parseFloat(document.getElementById('tempDiff').value);

    const Qroof = k * area * tempDiff / d;

    document.getElementById('result').innerText = `Total Heat Gain Through Roof: ${Qroof.toFixed(2)} W`;
}


function CHGOccupants() {
    const occupants = parseInt(document.getElementById('occupants').value);
    const Qoccupants = occupants * 100; // Each occupant contributes 100W

    document.getElementById('result').innerText = `Total Heat Gain from Occupants: ${Qoccupants} W`;
}


function CHGEquipments() {
    const Qwalls = parseFloat(document.getElementById('walls').value);
    const Qwindow = parseFloat(document.getElementById('window').value);
    const Qroof = parseFloat(document.getElementById('roof').value);
    const Qoccupants = parseFloat(document.getElementById('occupants').value);
    const Qcomputers = parseFloat(document.getElementById('computers').value);
    const Qlights = parseFloat(document.getElementById('lights').value);
    const Qfans = parseFloat(document.getElementById('fans').value);

    const Qtotal = Qwalls + Qwindow + Qroof + Qoccupants + Qcomputers + Qlights + Qfans;
    const tonnage = Qtotal / 3517;

    document.getElementById('result').innerHTML = `
        <p>Total Heat Gain: ${Qtotal.toFixed(2)} W</p>
        <p>Tonnage Required: ${tonnage.toFixed(2)} tons</p>
    `;
}


// Simulated user information (replace with actual user data handling)
const user = {
    name: "John Doe",
    email: "john.doe@example.com",
    role: "User"
};

// Display user information
document.getElementById('userInfo').innerHTML = `
    <p><strong>Name:</strong> ${user.name}</p>
    <p><strong>Email:</strong> ${user.email}</p>
    <p><strong>Role:</strong> ${user.role}</p>
`;





