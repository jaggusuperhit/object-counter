# Create virtual environment
python -m venv .venv

# Create tmp directory structure if it doesn't exist
New-Item -ItemType Directory -Force -Path tmp\model\rfcn\1
New-Item -ItemType Directory -Force -Path tmp\debug

# Download the model if it doesn't exist
if (-not (Test-Path tmp\model\rfcn\1\saved_model.pb)) {
    Write-Host "Downloading model..."
    Invoke-WebRequest -Uri "https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz" -OutFile "rfcn_model.tar.gz"
    
    # Extract using 7-Zip (assuming it's installed)
    # If 7-Zip is not available, you'll need to extract manually
    if (Get-Command "7z" -ErrorAction SilentlyContinue) {
        7z x rfcn_model.tar.gz -otmp
        7z x tmp\rfcn_model.tar -otmp
        
        # Move the model file
        Copy-Item -Path tmp\rfcn_resnet101_coco_2018_01_28\saved_model\saved_model.pb -Destination tmp\model\rfcn\1\
        
        # Clean up
        Remove-Item -Path rfcn_model.tar.gz
        Remove-Item -Path tmp\rfcn_model.tar
        Remove-Item -Path tmp\rfcn_resnet101_coco_2018_01_28 -Recurse
        
        Write-Host "Model downloaded successfully!"
    } else {
        Write-Host "7-Zip not found. Please extract the model manually:"
        Write-Host "1. Extract rfcn_model.tar.gz"
        Write-Host "2. Extract the resulting tar file"
        Write-Host "3. Copy saved_model.pb to tmp\model\rfcn\1\"
    }
} else {
    Write-Host "Model already exists, skipping download."
}

# Activate virtual environment and install dependencies
Write-Host "To activate the virtual environment, run: .\.venv\Scripts\Activate.ps1"
Write-Host "Then install dependencies with: pip install -r requirements.txt"

Write-Host "Setup completed!"
