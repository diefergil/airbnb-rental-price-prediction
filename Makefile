ONESHELL:
create_pipeline_component:
	cookiecutter -f https://github.com/diefergil/cookie-mlflow-step.git -o src


ONSESHELL:
download_clean_data:
	mlflow run . -P steps=download,basic_cleaning

################################################################
ONSESHELL:
list_mlflow_envs:
	conda info --envs | grep mlflow | cut -f1 -d" "

ONSESHELL:
clean_mlflow_envs:
	for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y;done

ONSESHELL:
grid_search:
	mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.rand om_forest.max_depth=10,50,100 modeling.random_forest.n_estimators=100,200,500 -m"