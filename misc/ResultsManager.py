import os


class ResultsManager:

    @staticmethod
    def get_project_dir():
        project_dir = os.path.dirname(__file__)
        project_dir = project_dir.replace("\\genetic_manager", "")
        project_dir = project_dir.replace("\\misc", "")
        return project_dir

    @staticmethod
    def create_results_folder_if_does_not_exists(project_dir):
        full_path = project_dir + "\\results"
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    @staticmethod
    def write_results(file_name, results):
        project_dir = ResultsManager.get_project_dir()
        ResultsManager.create_results_folder_if_does_not_exists(project_dir)
        full_file_name = file_name + ".txt"
        filename = os.path.join(project_dir, "results\\" + full_file_name)
        f = open(filename, "w+")
        f.write(results)
        f.close()
