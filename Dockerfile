FROM python:3.11
WORKDIR /app
COPY app/api/pip.requirements requirements.txt 
RUN pip install -r requirements.txt
COPY app/ .
 
#/secops/clients/cli
RUN pip install debugpy
#CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "secops/clients/cli/bper-client.py", "--action", "insert", "--safeName", "BPER__SAFE_1", "--safeMember", "LOB_Demo", "--accountsDescriptionJsonFile", "/tmp/accounts"]
CMD sh -c "python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client $DEBUG_SCRIPT"
