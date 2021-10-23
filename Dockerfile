FROM node:alpine as builder
USER node
WORKDIR '/home/node'
COPY package.json .
RUN npm install
COPY --chown=node:node . .
RUN npm run build



FROM nginx
COPY --from=builder /home/node/build /usr/share/nginx/html

