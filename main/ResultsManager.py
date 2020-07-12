import os


class ResultsManager:

    @staticmethod
    def get_results_dir():
        project_dir = os.path.dirname(__file__)
        project_dir = project_dir.replace("genetic_manager", "")
        project_dir = project_dir.replace("misc", "")
        project_dir = project_dir.replace("main", "")
        return os.path.join(project_dir, "results")

    @staticmethod
    def get_result_file_path(file_name, results_dir=None):
        results_dir = results_dir if results_dir else ResultsManager.get_results_dir()
        file_name = file_name if ".json" in file_name else file_name + ".json"
        return os.path.join(results_dir, file_name)

    @staticmethod
    def write_results(file_name, results):
        results_dir = ResultsManager.get_results_dir()
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        results_file_path = ResultsManager.get_result_file_path(file_name, results_dir)
        try:
            f = open(results_file_path, "w+", encoding="utf-8")
            f.write(results)
            f.close()
        except Exception as e:
            print("Error saving results: " + str(e))

    @staticmethod
    def read_results(file_name):
        result_file_path = ResultsManager.get_result_file_path(file_name)
        if os.path.exists(result_file_path):
            try:
                f = open(result_file_path, "r")
                results = f.read()
                return results, None
            except Exception as e:
                return None,  "Error loading results file: " + str(e)
        return None, "Results file does not exists or not located on results folder."
