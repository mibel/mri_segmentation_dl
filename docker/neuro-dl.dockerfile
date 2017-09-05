FROM gcr.io/tensorflow/tensorflow:latest-gpu-py3

ENV LAST_UPDATED 21-07-2017
RUN apt-get update && apt-get install -y \
	git \
	wget

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh 
RUN ./Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda3
RUN chmod -R 777 /miniconda3
RUN rm ./Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/miniconda3/bin:${PATH}"

RUN pip install scikit-learn==0.18.2
RUN pip install pandas==0.20.2
RUN pip install matplotlib==2.0.2
RUN pip install seaborn==0.7.0
RUN pip install nibabel==2.1.0
RUN pip install tqdm==4.14.0
RUN pip install scikit-image==0.13.0
RUN pip install snakemake==3.13.3
RUN pip install tensorflow-gpu==1.2.1
