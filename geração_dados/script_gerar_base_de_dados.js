const fetch = require('node-fetch')

const serverUrl = 'http://localhost:3000'
const pokeApiUrl = 'https://pokeapi.co/api/v2'

function getHeightCategory (height) {
  if (height <= 7) return 'short'
  if (height <= 17) return 'medium'
  return 'tall'
}

function getWeightInKg (weight) {
  return weight / 10
}

function findSpeciesNode (chain, speciesName) {
  if (chain.species.name === speciesName) {
    return chain
  }

  for (const evolution of chain.evolves_to) {
    const foundNode = findSpeciesNode(evolution, speciesName)

    if (foundNode) {
      return foundNode
    }
  }

  return null
}

async function fetchJson (url) {
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status} for ${url}`)
  }

  return response.json()
}

async function buildPokemonData (pokemonListItem, fallbackId) {
  const pokemon = await fetchJson(pokemonListItem.url)
  const species = await fetchJson(pokemon.species.url)
  const evolutionChain = await fetchJson(species.evolution_chain.url)
  const currentSpeciesNode = findSpeciesNode(evolutionChain.chain, species.name)
  const types = pokemon.types
    .sort((a, b) => a.slot - b.slot)
    .map(({ type }) => type.name)

  return {
    id: pokemon.id || fallbackId,
    name: pokemon.name,
    url: pokemonListItem.url,
    picture: pokemon.sprites.front_default || `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.id || fallbackId}.png`,
    types,
    generation: species.generation.name,
    color: species.color.name,
    habitat: species.habitat ? species.habitat.name : null,
    has_multiple_types: types.length > 1,
    evolves_from: species.evolves_from_species ? species.evolves_from_species.name : null,
    doesnt_evolve: currentSpeciesNode ? currentSpeciesNode.evolves_to.length === 0 : null,
    is_legendary: species.is_legendary,
    is_mythical: species.is_mythical,
    height_category: getHeightCategory(pokemon.height),
    weight: {
      hectograms: pokemon.weight,
      kilograms: getWeightInKg(pokemon.weight)
    }
  }
}

async function go () {
  try {
    const pokemons = await fetchJson(`${pokeApiUrl}/pokemon?limit=151`)

    for (const [i, pokemon] of pokemons.results.entries()) {
      try {
        const pokemonData = await buildPokemonData(pokemon, i + 1)

        await fetch(`${serverUrl}/pokemon`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(pokemonData)
        })

        console.log(`Posted info about pokemon #${pokemonData.id} ${pokemonData.name}`)
      } catch (error) {
        console.error('Error while posting pokemon to json server', error)
      }
    }
  } catch (error) {
    console.error('Error while getting pokemon from pokeapi', error)
  }
}

go()
