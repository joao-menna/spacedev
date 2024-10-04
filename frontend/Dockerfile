FROM node:20-alpine as build

WORKDIR /app

COPY ./package.json .
COPY ./yarn.lock .

RUN npm i -g yarn; \
    yarn;

COPY . .

RUN yarn build

FROM nginx:1.27.0-bookworm

COPY ./nginx /etc/nginx

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
