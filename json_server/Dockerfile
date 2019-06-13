FROM node:8

COPY db.json /tmp/json_server/db.json
COPY index.js /tmp/json_server/index.js

RUN npm install -g json-server

EXPOSE 3000

CMD json-server --watch /tmp/json_server/index.js --port 3000 --host 0.0.0.0

