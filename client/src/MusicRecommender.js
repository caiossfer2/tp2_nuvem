import React, { useState } from "react";
import axios from "axios";
import Papa from "papaparse";
import {
  Box,
  Button,
  Checkbox,
  Container,
  FormControlLabel,
  Grid2,
  Typography,
} from "@mui/material";

const URL = "http://localhost:32051/api/recommend";

function MusicRecommender() {
  const [songs, setSongs] = useState([]);
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [recommendations, setRecommendations] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const songsPerPage = 10;

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    Papa.parse(file, {
      header: true,
      complete: (results) => {
        setSongs(results.data);
      },
    });
  };

  const getRecommendations = () => {
    axios
      .post(URL, {
        songs: selectedSongs.map((song) => song.track_name),
      })
      .then((response) => {
        setRecommendations(response.data);
      })
      .catch((error) => {
        console.error("There was an error making the request:", error);
      });
  };

  const indexOfLastSong = currentPage * songsPerPage;
  const indexOfFirstSong = indexOfLastSong - songsPerPage;
  const currentSongs = songs.slice(indexOfFirstSong, indexOfLastSong);

  return (
    <Container>
      <Grid2 mt="8px">
        <Typography variant="h3">Playlist Recommender</Typography>
        {!recommendations && (
          <Grid2>
            {songs.length === 0 && (
              <Grid2 mt={"24px"}>
                <Typography variant="h5">
                  Selecione o arquivo contendo as músicas
                </Typography>
                <input type="file" accept=".csv" onChange={handleFileUpload} />
              </Grid2>
            )}

            {songs.length > 0 && (
              <Grid2 mt="24px" display="flex" flexDirection="column" gap="8px">
                <Typography variant="h5">Escolha as músicas</Typography>
                <Box>
                  {currentSongs.map((song, index) => (
                    <Box>
                      <FormControlLabel
                        key={index}
                        control={
                          <Checkbox
                            checked={selectedSongs.some(
                              (s) => s.track_name === song.track_name
                            )}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedSongs([...selectedSongs, song]);
                              } else {
                                setSelectedSongs(
                                  selectedSongs.filter(
                                    (s) => s.track_name !== song.track_name
                                  )
                                );
                              }
                            }}
                          />
                        }
                        label={`${song.artist_name} - ${song.track_name}`}
                      />
                    </Box>
                  ))}
                </Box>
                <Grid2>
                  <Button
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                  >
                    Anterior
                  </Button>
                  <span> Página {currentPage} </span>
                  <Button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={indexOfLastSong >= songs.length}
                  >
                    Próximo
                  </Button>
                </Grid2>
                <Box>
                  <Button variant="contained" onClick={getRecommendations}>
                    Obter recomendações
                  </Button>
                </Box>
              </Grid2>
            )}
          </Grid2>
        )}
        {recommendations && (
          <Grid2>
            <Typography variant="h5" mt="24px">
              Playlist recomendada
            </Typography>
            <p>Data modelo: {recommendations.model_date}</p>
            <p>Versão: {recommendations.version}</p>
            <ul>
              {recommendations.songs.map((song, index) => (
                <li key={index}>{song}</li>
              ))}
            </ul>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => setRecommendations(null)}
            >
              Voltar
            </Button>
          </Grid2>
        )}
      </Grid2>
    </Container>
  );
}

export default MusicRecommender;
