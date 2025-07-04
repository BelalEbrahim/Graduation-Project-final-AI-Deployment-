document.addEventListener('DOMContentLoaded', function() {
    // Salary Prediction
    document.getElementById('salaryForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        fetch('/predict_salary', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            const resultDiv = document.getElementById('salaryResult');
            if (result.error) {
                resultDiv.innerHTML = `
                    <div class="result-box error">
                        <h5 class="mb-2">Error</h5>
                        <p>${result.error}</p>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `
                    <div class="result-box success">
                        <h5 class="mb-2">Predicted Salary</h5>
                        <h3 class="text-primary">$${parseFloat(result.predicted_salary).toLocaleString()}</h3>
                    </div>
                `;
            }
        });
    });

    // Startup Prediction
    document.getElementById('startupForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        fetch('/predict_startup', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            const resultDiv = document.getElementById('startupResult');
            if (result.error) {
                resultDiv.innerHTML = `
                    <div class="result-box error">
                        <h5 class="mb-2">Error</h5>
                        <p>${result.error}</p>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `
                    <div class="result-box success">
                        <h5 class="mb-2">Startup Analysis</h5>
                        <p>Prediction: <strong>${result.prediction}</strong></p>
                        <div class="progress my-3" style="height: 20px;">
                            <div class="progress-bar bg-success" role="progressbar" 
                                 style="width: ${result.confidence * 100}%"
                                 aria-valuenow="${result.confidence * 100}"
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                ${Math.round(result.confidence * 100)}% Confidence
                            </div>
                        </div>
                    </div>
                `;
            }
        });
    });

    // Job Recommendations
    document.getElementById('jobsForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        fetch('/recommend_jobs', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            const resultDiv = document.getElementById('jobsResult');
            if (result.error) {
                resultDiv.innerHTML = `
                    <div class="result-box error">
                        <h5 class="mb-2">Error</h5>
                        <p>${result.error}</p>
                    </div>
                `;
            } else {
                const jobsHTML = result.recommendations.map(job => `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${job.title}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${job.company_name}</h6>
                            <p class="card-text">${job.description.substring(0, 200)}...</p>
                        </div>
                    </div>
                `).join('');
                
                resultDiv.innerHTML = `
                    <div class="result-box recommendations">
                        <h5 class="mb-3">Job Recommendations</h5>
                        ${jobsHTML || '<p>No recommendations found</p>'}
                    </div>
                `;
            }
        });
    });
});