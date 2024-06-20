document.getElementById('polling_station').addEventListener('input', function() {
    var pollingStationName = this.value;
    if (pollingStationName.length > 0) {
        fetch('/search?polling_station=' + encodeURIComponent(pollingStationName))
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('ward').value = '';
                    document.getElementById('constituency').value = '';
                } else {
                    document.getElementById('ward').value = data.ward;
                    document.getElementById('constituency').value = data.constituency;
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('ward').value = '';
        document.getElementById('constituency').value = '';
    }
});
