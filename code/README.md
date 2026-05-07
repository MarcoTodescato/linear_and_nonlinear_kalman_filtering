<div align='center'>
  <h1><b>LINEAR and NONLINEAR KALMAN FILTERING</b></h1>
</div>

This is Python-based repo for the DAUSY course on Linear and Nonlinear Kalman Filtering.

It contains some minimal code examples and a dockerized environment to work with
Jupyter notebooks.

---

## 📁 Project Structure

```bash
root/
├── docker/                       # Container definitions for reproducible workflow
│   ├── Dockerfile
│   └── docker-compose.yml
├── src/
├── notebooks/                    # folder containing some notebooks
├── requirements.txt
├── setup.py
├── Makefile
├── README.md
```

---

## 📋 Prerequisites

Assuming installation on Ubuntu 22.04 or higher.

Tested on Ubuntu 24.04 running on WSL (Windows Subsystem for Linux)

Other OS are not convered nor tested.

- Make: if not installed run `sudo apt update & sudo apt install build-essential`
- [Python](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/) : follow instruction to install [docker engine](https://docs.docker.com/engine/install/ubuntu/) and [post-installation setup](https://docs.docker.com/engine/install/linux-postinstall/). Using [apt repo's](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) is recommended.
- [Docker Compose](https://docs.docker.com/compose/): using [apt repo's](https://docs.docker.com/compose/install/linux/#install-using-the-repository) recommended.

For Windows users, using WSL is recommended. Another option is to use native Docker Desktop for Windows.

---

## 💻 How to Run

### ▶️ Method 1: Using Docker (highly recommended)

From inside this repo root (where the `Makefile` is located)

```bash
make notebook
```

The first time this may take some time in order to build the docker image.
Then open your browser at: http://localhost:8888
You'll find all notebooks in the /notebooks folder and can directly run them.
To stop the container:

```bash
CTRL + C
```

### ▶️ Method 2: Run Locally (No Docker)

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Start coding (Jupyter Notebook):

```bash
jupyter notebook
```

PS. if preferred, also python scripts can be used.


### Method 3: Develop your own code-package

If you want to develop dedicated functions or classes, you can put them inside
the `linear_and_nonlinear_kf` foder, organizing python modules into files or
sub-packages, as per your preferred choice.

In this case, if using Docker, uncomment the lines

```Dockerfile
# # Locall install the package
# RUN pip install -e .
```

in the Dockerifle to install the package in the container at build time.

If using a local python environment, install the package manually.

## 🗨️ Contact

Marco Todescato // marco.todescato@fraunhofer.it  (mrc.todescato@gmail.com)
