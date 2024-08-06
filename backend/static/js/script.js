document.addEventListener('DOMContentLoaded', function() {
    function fetchPackets() {
        fetch('/api/packets')
            .then(response => response.json())
            .then(data => {
                updatePacketTable(data);
            })
            .catch(error => console.error('Error fetching packets:', error));
    }

    function updatePacketTable(packets) {
        const tableBody = document.getElementById('packet-table-body');
        tableBody.innerHTML = ''; // Clear previous content

        packets.forEach(packet => {
            const row = document.createElement('tr');

            // Create cells for packet info
            const lengthCell = document.createElement('td');
            lengthCell.textContent = packet.info.length;
            row.appendChild(lengthCell);

            const srcIpCell = document.createElement('td');
            srcIpCell.textContent = packet.info.src_ip;
            row.appendChild(srcIpCell);

            const dstIpCell = document.createElement('td');
            dstIpCell.textContent = packet.info.dst_ip;
            row.appendChild(dstIpCell);

            const protocolCell = document.createElement('td');
            protocolCell.textContent = packet.info.protocol;
            row.appendChild(protocolCell);

            const srcPortCell = document.createElement('td');
            srcPortCell.textContent = packet.info.src_port;
            row.appendChild(srcPortCell);

            const dstPortCell = document.createElement('td');
            dstPortCell.textContent = packet.info.dst_port;
            row.appendChild(dstPortCell);

            const flagsCell = document.createElement('td');
            flagsCell.textContent = packet.info.flags;
            row.appendChild(flagsCell);

            const classificationCell = document.createElement('td');
            classificationCell.textContent = packet.classification;
            row.appendChild(classificationCell);

            tableBody.appendChild(row);
        });
    }

    // Fetch packets every 5 seconds
    setInterval(fetchPackets, 5000);
});
