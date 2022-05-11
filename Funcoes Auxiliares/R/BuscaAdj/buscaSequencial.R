library(purrr)
library(dplyr)
library(tidyr)

dados10=read.table("/home/jailson/Downloads/dados.txt",
  sep=" ", 
  dec=".",
  header = TRUE)

fun <- function(dados){    
  id_list <- unique(as.character(dados$clientID))
  output <- data.frame()
  for (user in id_list){
    dados %>% filter(clientID == user) -> filtro
    filtro %>% arrange(hora) -> filtro
    nrows <- nrow(filtro)
    if (nrows == 1){output <- rbind(output, filtro); next}
    output <- rbind(output, buscaSequencial(filtro))
    print(paste("Linhas no dataframe", nrow(output)))
  }
  
  return(output)
}

buscaSequencial <- function(d.f){
  repetidos <- rep(0, length(d.f$página))
  x = 0
  if (nrow(d.f)>1){
    for (i in 2:nrow(d.f)-1){ 
      x[i] = c(d.f$página[i] != d.f$página[i+1])
    }
  }
  if (length(unique(d.f$página)) == 1 ){
    return(d.f[1,])
  }
  else if(nrow(d.f) == sum(x)+1) return(d.f)
  else if (length(unique(d.f$página)) > 1){
    for (i in (2:nrow(d.f))-1){
    if (d.f$página[i+1] == d.f$página[i]){
      repetidos[c(i, i+1)] <- c(1, -1)     
      print(repetidos)
      d.f <- d.f[-which(repetidos == -1),]   #trocar por -1?
      print(nrow(d.f))
      return (buscaSequencial(d.f))
    }
    
    print("_*__*__*__*__*__*__*__*__*__*_*__*__*__*__*__*__*__*__*__*__")
    print(repetidos)
    print(d.f)
    print(length(repetidos))
    print("-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--")
    }
  }
} 



dados10 %>% nest(dados = !data) -> dados10
lista_semduplicatas  = lapply(dados10$dados, fun)
df_limpo = do.call(rbind, lista_semduplicatas)

