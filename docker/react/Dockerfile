FROM node

COPY ./frontend/public/ /blog/frontend/public
COPY ./frontend/src/ /blog/frontend/src
COPY ./frontend/package.json /blog/frontend
COPY ./frontend/tailwind.config.js blog/frontend
COPY ./frontend/tsconfig.json blog/frontend

WORKDIR /blog/frontend

RUN npm install

EXPOSE 14777

CMD ["npm", "start"]