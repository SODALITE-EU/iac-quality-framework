# iac-quality-framework

## How to install and import modules locally

First, install the necessary dependencies with the command:

```pip3 install -r requirements.txt```

You can install the package locally from the project root folder with the command:

```pip3 install . ```

Once the installation succeed you can import the module in your python application with:

```python
import ansiblemetrics
```
## Docker Image Building and Usage
```
sudo docker build -t sodalite/iacmetrics .
sudo docker run -p 5000:5000 -d --name=iacmetricsAPI sodalite/iacmetrics
sudo docker start iacmetricsAPI
sudo docker logs iacmetricsAPI
sudo docker stop iacmetricsAPI
sudo docker rm  iacmetricsAPI
sudo docker rmi sodalite/iacmetrics
```
