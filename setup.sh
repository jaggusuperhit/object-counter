#!/bin/bash

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create tmp directory structure if it doesn't exist
mkdir -p tmp/model/rfcn/1
mkdir -p tmp/debug

# Download the model if it doesn't exist
if [ ! -f tmp/model/rfcn/1/saved_model.pb ]; then
    echo "Downloading model..."
    wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
    tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
    rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
    chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
    mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/rfcn/1
    rm -rf tmp/rfcn_resnet101_coco_2018_01_28
    echo "Model downloaded successfully!"
else
    echo "Model already exists, skipping download."
fi

echo "Setup completed successfully!"
echo "To activate the virtual environment, run: source .venv/bin/activate"
