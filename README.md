# NIQ Innovation Enablement - Challenge 1 (Object Counting)

The goal of this repo is demonstrate how to apply Hexagonal Architecture in a ML based system.

This application consists in a Flask API that receives an image and a threshold and returns the number of objects detected in the image.

The application is composed by 3 layers:

- **entrypoints**: This layer is responsible for exposing the API and receiving the requests. It is also responsible for validating the requests and returning the responses.

- **adapters**: This layer is responsible for the communication with the external services. It is responsible for translating the domain objects to the external services objects and vice-versa.

- **domain**: This layer is responsible for the business logic. It is responsible for orchestrating the calls to the external services and for applying the business rules.

The model used in this example has been taken from
[IntelAI](https://github.com/IntelAI/models/blob/master/docs/object_detection/tensorflow_serving/Tutorial.md)


## Instructions to configure this project
```
# Download the rfcn model
wget https://storage.googleapis.com/intel-optimized-tensorflow/models/v1_8/rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
tar -xzvf rfcn_resnet101_fp32_coco_pretrained_model.tar.gz -C tmp
rm rfcn_resnet101_fp32_coco_pretrained_model.tar.gz
chmod -R 777 tmp/rfcn_resnet101_coco_2018_01_28
mkdir -p tmp/model/rfcn/1
mv tmp/rfcn_resnet101_coco_2018_01_28/saved_model/saved_model.pb tmp/model/rfcn/1
rm -rf tmp/rfcn_resnet101_coco_2018_01_28
```

## Setup and run Tensorflow Serving

```

# For unix systems
cores_per_socket=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | xargs`
num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | xargs`
num_physical_cores=$((cores_per_socket * num_sockets))

docker rm -f tfserving
docker run \
    --name=tfserving \
    -p 8500:8500 \
    -p 8501:8501 \
    -v "$(pwd)\tmp\model:/models" \
    -e OMP_NUM_THREADS=$num_physical_cores \
    -e TENSORFLOW_INTER_OP_PARALLELISM=2 \
    -e TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores \
    intel/intel-optimized-tensorflow-serving:2.8.0 \
    --model_config_file=/models/model_config.config

# For Windows (Powershell)
$num_physical_cores=(Get-WmiObject Win32_Processor | Select-Object NumberOfCores).NumberOfCores
echo $num_physical_cores

docker rm -f tfserving
docker run `
    --name=tfserving `
    -p 8500:8500 `
    -p 8501:8501 `
    -v "$pwd\tmp\model:/models" `
    -e OMP_NUM_THREADS=$num_physical_cores `
    -e TENSORFLOW_INTER_OP_PARALLELISM=2 `
    -e TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores `
    intel/intel-optimized-tensorflow-serving:2.8.0 `
    --model_config_file=/models/model_config.config
```


## Database Options

### Option 1: Run local MongoDB

```bash
docker rm -f test-mongo
docker run --name test-mongo --rm -p 27017:27017 -d mongo:latest
```

### Option 2: Use MongoDB Atlas

1. Create a MongoDB Atlas account at https://www.mongodb.com/cloud/atlas/register
2. Create a new cluster (the free tier is sufficient)
3. Create a database user with read/write permissions
4. Add your IP address to the IP Access List
5. Get your connection string from the Atlas dashboard
6. Set the connection string as an environment variable:

```bash
# Unix
export MONGO_CONNECTION_STRING="mongodb+srv://username:password@cluster.mongodb.net/"

# Powershell
$env:MONGO_CONNECTION_STRING="mongodb+srv://username:password@cluster.mongodb.net/"
```


## Setup

### Option 1: Using setup scripts

#### Unix/Linux/Mac
```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh

# Activate the virtual environment
source .venv/bin/activate
```

#### Windows (PowerShell)
```powershell
# Run the setup script
.\setup.ps1

# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using Makefile (Unix/Linux/Mac)
```bash
# Run the setup target
make setup

# Activate the virtual environment
source .venv/bin/activate
```

### Option 3: Manual setup
```bash
# Python >= 3.0
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the application

### Option 1: Using Makefile

```bash
# Run with fake services (development mode)
make run-dev

# Run with local MongoDB and TensorFlow Serving
make run-prod

# Run with MongoDB Atlas and TensorFlow Serving
make run-atlas
```

### Option 2: Using Python directly

#### Using fakes
```
python -m counter.entrypoints.webapp
```

#### Using real services in docker containers

```
# Unix - with local MongoDB
ENV=prod python -m counter.entrypoints.webapp

# Powershell - with local MongoDB
$env:ENV = "prod"
python -m counter.entrypoints.webapp

# Unix - with MongoDB Atlas
ENV=atlas python -m counter.entrypoints.webapp

# Powershell - with MongoDB Atlas
$env:ENV = "atlas"
python -m counter.entrypoints.webapp
```

## Call the service

### Object Count Endpoint

```shell script
 curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://0.0.0.0:5000/object-count
 curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://0.0.0.0:5000/object-count
```

### Predictions Endpoint

```shell script
 curl -F "threshold=0.9" -F "file=@resources/images/boy.jpg" http://0.0.0.0:5000/predictions
 curl -F "threshold=0.9" -F "file=@resources/images/cat.jpg" http://0.0.0.0:5000/predictions
 curl -F "threshold=0.9" -F "file=@resources/images/food.jpg" http://0.0.0.0:5000/predictions
```

## Run the tests

### Using pytest directly
```
pytest
```

### Using Makefile
```
make test
```