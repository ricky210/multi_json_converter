FROM python:latest

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org  --trusted-host pypi.python.org pandas openpyxl\
    && mkdir -p /opt/app/server_unittest_converter
COPY ./ /opt/app/server_unittest_converter/server_unittest_converter
WORKDIR /opt/app/server_unittest_converter
ENTRYPOINT ["python3", "-m", "server_unittest_converter"]
