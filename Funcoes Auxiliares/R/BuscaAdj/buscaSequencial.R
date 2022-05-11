library(purrr)
library(dplyr)
library(tidyr)
library(future.apply)

dados10 = read.table("/home/jailson/Downloads/dados.txt",
  sep=" ", 
  dec=".",
  header = TRUE)

log = function(d.f, .s){
    print(nrow(d.f))
    print("_*__*__*__*__*__*__*__*__*__*_*__*__*__*__*__*__*__*__*__*__")
    print(d.f)
    print(.s)
    print("-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--")
}

all_distinct <- function(d.f){
  x = 0
  if (nrow(d.f) > 1){
    for (i in 2:nrow(d.f)-1){ 
      x[i] = c(d.f$página[i] != d.f$página[i+1])
    }
  }
  return(sum(x))
}

busca_duplicados <- function(d.f){
  repetidos <- rep(0, length(d.f$página))
  for (i in (2:nrow(d.f))-1){
    if (d.f$página[i+1] == d.f$página[i]){
      repetidos[c(i, i+1)] <- c(1, -1)     
      print(repetidos)
      d.f <- d.f[-which(repetidos == -1),]   #trocar por -1? 
      log(d.f, repetidos)
      return (remove_duplicados(d.f))
    } 
  }
}

remove_duplicados <- function(d.f){
  #se todos os elementos sao iguais, basta utilizar o primeiro
  if (length(unique(d.f$página)) == 1 ) return(d.f[1,])

  #se todos sao distintos dois a dois retorna o df todo
  else if (nrow(d.f) == all_distinct(d.f)+1 ) return(d.f)

  #se existem pelo menos dois distintos no df chama a func. busca_duplicados
  else if (length(unique(d.f$página)) > 1 ) busca_duplicados(d.f) 
}

apply_fun_split <- function(d.f, .f){    
  all_distinct
  busca_duplicados
  remove_duplicados
  id_list <- unique(as.character(d.f$clientID))
  output <- data.frame()
  d.f %>% split(~clientID) %>% 
          lapply(arrange, hora) -> output
  output <- do.call(rbind, future_lapply(output, .f))
  return(output)
}



#separa por data
df_data = split(dados10, ~data)

#elimina as dulpicatas
a1 = Sys.time()
## rodar em paralelo em 5 sessoes do R
plan(multisession, workers = 5)
l = future_lapply( df_data,
                   apply_fun_split, 
                   remove_duplicados)
b1 = Sys.time()
b1-a1


