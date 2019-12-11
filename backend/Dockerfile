FROM node:12

# make the 'app' folder the current working directory
WORKDIR /usr/src/app

# copy both 'package.json' and 'package-lock.json'
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# expose port
EXPOSE 3000

ENV DEAL_REG_DB_URL=postgresql://@localhost:5432/DealRegDB

CMD ["npm", "start"]