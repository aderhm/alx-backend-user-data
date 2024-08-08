#!/usr/bin/node
/**
 * The first positional argument passed is the Movie ID
 * Display one character name per line in the same order
 * as  list in the /films/ endpoint
 * Uses the Star wars API.
 */

const request = require('request');

const id = process.argv[2];

if (!id) {
  console.error('Usage: ./0-starwars_characters.js <ID>');
  process.exit(1);
}

const url = `https://swapi-api.alx-tools.com/api/films/${id}/`;

function fetch (url) {
  return new Promise((resolve, reject) => {
    request(url, (error, response, body) => {
      if (error) {
        reject(error);
      } else if (response.statusCode !== 200) {
        reject(new Error(`Status Code: ${response.statusCode}`));
      } else {
        resolve(JSON.parse(body));
      }
    });
  });
}

fetch(url)
  .then(filmData => {
    const charactersEndPoints = filmData.characters;
    const characterPromises = charactersEndPoints.map(charactersEndPoint => fetch(charactersEndPoint));
    return Promise.all(characterPromises);
  })
  .then(characters => {
    characters.forEach(character => {
      console.log(character.name);
    });
  })
  .catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
