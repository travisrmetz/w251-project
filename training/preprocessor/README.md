[_Return to the white paper_](https://github.com/travisrmetz/w251-project#Train)

# Celestial Inference at the Edge
## W251 - Final Project - Metz/Tozzi - Summer 2020
### Setting up the Image Preprocessing Container on a Virtual Server

This section provides basic steps to set up the preprocessor described in section 5 of our white paper.

### Build the Container

Assuming that you have pulled the repo to the virtual server, the following commands will build the container.

```
cd /root/w251-project/training/preprocessor
docker build -t preprocessor -f preprocessor.dockerfile .
```

If needed, make a new directory to store the processed Numpy arrays.

```
mkdir <directory>
```

### Run the Container
Edit the `preprocessor.yml` file as necessary, spin up a container, and preprocess using the following commands.

```
docker run --name preproc -dit -v <train/validation directory>:<train/validation directory> -v <test directory>:<test directory> -v <directory where you want the arrays>:<directory where you want the arrays> preprocessor
docker exec -d preproc python3 preprocessor.py
```

### Tearing Down the Container
Once the preprocessing is complete and you have verified that the `.npy` files are where you expect, tear down the container.

```
docker stop preproc
docker rm preproc
