document.getElementById('polling_station').addEventListener('change', function() {
    var pollingStationId = this.value;
    
    fetch(`/get_wards_and_constituency?polling_station_id=${pollingStationId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('ward').value = data.ward_id;
            document.getElementById('constituency').value = data.constituency_id;
        });
});
