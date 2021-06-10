#include <stdio.h>
#include <math.h>
/************************************************/
/******programa pra preencher uma matriz NxN******/
/************************************************/
float FillMatrix(int n){
	float matriz[n][n];
	int valor = 0;
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			printf("entre com o elemento  %a%d%d \n",i+1,j+1);
			scanf("%f", &matriz[i][j]);
		};
	};
};

/************************************************/
/* calcular menor */
/************************************************/
	void menor(float b[100][100],float a[100][100],int i,int n){
		int j,l,h=0,k=0;
		for(l=1;l<n;l++)	
			for( j=0;j<n;j++){
				if(j == i)
					continue;
				b[h][k] = a[l][j];
				k++;
				if(k == (n-1)){
					h++;
					k=0;
				};
			};
		};
/************************************************/
/*calcular determinante*/
/************************************************/

/************************************************/
/* inverter matriz */
/************************************************/


		int main(){
			int entrada = 0;
			int notas[3];
			int flag = 0;
			float media =0 ;
			float matx;
			int N = 0;
			while(!flag){
				printf("\n############### digite uma das opções ############### \n");

				printf("############### 0: Sair ###############\n");

				printf("############### 2: Volta Para o Inicio ###############\n");

				printf("############### 4: Entre os valores da matriz:############### \n");

				scanf("%d", &entrada);
				switch(entrada){
					case 2:
					break;
					case 3:
					for(int i = 0; i < 3; i++){
						printf("Entre com a %d-ésima nota \n",i+1);
						scanf("%d", &notas[i]);
					};
					media = (notas[0]+notas[1]+notas[2])/3;
					printf("a media das notas eh\n: %.4f \n",media);
					break;
					case 0:
					flag = 1;

					case 4:
					printf("preencha a dimensao da matriz quadrada: \n");
					scanf("%d",&N);
					matx = FillMatrix(N);				
					for(int i; i<N;i++){
						for(int j; j<N; j++){
							printf("%d",matx);
						};
					};

				};
			};

			return(0);
		}
