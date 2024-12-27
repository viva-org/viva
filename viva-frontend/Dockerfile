FROM node:20.17.0 as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine as production-stage
# 创建 ssl 目录，这一步之后把 ssh 证书粘贴到 /etc/nginx/ssl 目录下
# RUN mkdir -p /etc/nginx/ssl
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
