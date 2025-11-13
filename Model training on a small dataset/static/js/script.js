document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('preview').style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        document.getElementById('preview').style.display = 'none';
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById('fileInput');
    formData.append('file', fileInput.files[0]);

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    document.getElementById('submitBtn').disabled = true;

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;

        if (data.error) {
            document.getElementById('result').className = 'mt-3 alert alert-danger';
            document.getElementById('result').innerHTML = '<strong>Error:</strong> ' + data.error;
        } else {
            document.getElementById('result').className = 'mt-3 alert alert-success';
            document.getElementById('result').innerHTML = `<strong>Recognized:</strong> ${data.person}<br><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%`;
        }
        document.getElementById('result').style.display = 'block';
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
        document.getElementById('result').className = 'mt-3 alert alert-danger';
        document.getElementById('result').innerHTML = '<strong>Error:</strong> Something went wrong.';
        document.getElementById('result').style.display = 'block';
    });
});
