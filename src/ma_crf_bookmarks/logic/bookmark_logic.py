import numpy as np
import pandas as pd
import pymupdf


class MainLogic:
    def __init__(self):

        self.default_value: int = 10

    def start_logic(self, crf_path: str, sds_path: str, output_path: str) -> str:

        self.create_bookmarks(crf_path, sds_path, output_path)

        return "Finished"

    def toc_to_bookmark_dict(self, toc_input: list) -> dict:
        # level_1 = [(i, b) for (i, b) in enumerate(toc_input) if b[0] == 1]

        form_start_numbers = [b[2] for b in toc_input]

        form_start_labels = [" (".join(b[1].split(" (")[:-1]) for b in toc_input]
        # form_start_labels = [b[1] for b in toc_start]
        form_start_names = [b[1].split(" (")[-1].split(")")[0] for b in toc_input]

        input_bookmarks_dict = {}
        for name, page, label in zip(form_start_names, form_start_numbers, form_start_labels):
            # ML 20-Mar-26: correction for appendix
            if "Appendix" in name:
                label = name
            if label in input_bookmarks_dict.keys():
                input_bookmarks_dict[label].append((page, name))
            else:
                input_bookmarks_dict[label] = [(page, name)]
        return input_bookmarks_dict

    def get_form_visits(self, sds: pd.DataFrame, form_label: str, visit_labels: list[str]):
        # extract the visit/forms for a form
        sds_entry = sds[sds["Form Label"] == form_label]
        if not sds_entry.empty:
            visit_and_names = []
            for _, row in sds_entry.iterrows():
                form_name = row["Form Name"]
                mask = row.notna().to_numpy()[2:]
                form_visits = np.array(visit_labels)[mask].tolist()
                visit_and_names.append((form_name, form_visits))
            return visit_and_names
        else:
            print("No entry in sds file:", form_label)

    def create_bookmarks_form(
        self, sds: pd.DataFrame, input_bookmarks_dict: dict, visit_labels: list
    ) -> list:
        # iterate over the form lables alphabeticaly
        form_labels = list(input_bookmarks_dict.keys())
        form_labels.sort()

        new_toc_by_form = []
        # add first level bookmark
        new_toc_by_form.append([1, "By Form", 1])

        for form_label in form_labels:
            org_bm = input_bookmarks_dict[form_label]

            # form_name:page
            form_name_page_dict = {name: page for page, name in org_bm}

            # get all visits for the form
            visit_and_names = self.get_form_visits(sds, form_label, visit_labels)

            # first page for form_name
            first_page = org_bm[0][0]

            # 2-level bookmark - set to first form with the form_label
            new_toc_by_form.append([2, form_label, first_page])

            if visit_and_names:
                # 3-level bookmark
                for form_name, visit_list in visit_and_names:
                    for v in visit_list:
                        new_toc_by_form.append([3, v, form_name_page_dict[form_name]])
            else:
                new_toc_by_form.append([3, "Appendix", form_name_page_dict[form_label]])
                print(f"CAVE for {form_label} no visits found")
        return new_toc_by_form

    def create_bookmarks_visit(
        self, sds: pd.DataFrame, input_bookmarks_dict: dict, visit_labels: list
    ) -> list:
        new_toc_by_visit = []

        # add 1-level bookmark
        new_toc_by_visit.append([1, "By Visit", 1])

        for visit in visit_labels:
            # get sds informaiton by visit - sort alphabeticaly
            sds_visit = sds[sds[visit].notna()][["Form Label", "Form Name"]]
            sds_visit = sds_visit.sort_values(by="Form Label", ascending=True)

            # get first entry by visit
            first_label = sds_visit.iloc[0]["Form Label"]
            first_name = sds_visit.iloc[0]["Form Name"]
            org_bm = input_bookmarks_dict[first_label]
            form_name_page_dict = {name: page for page, name in org_bm}  # form_name:page
            fist_page = form_name_page_dict[first_name]

            # add 2-level bookmark
            new_toc_by_visit.append([2, visit, fist_page])

            # add 3-level bookmarks
            for _, row in sds_visit.iterrows():
                org_bm = input_bookmarks_dict[row["Form Label"]]
                form_name_page_dict = {name: page for page, name in org_bm}  # form_name:page
                page = form_name_page_dict[row["Form Name"]]
                new_toc_by_visit.append([3, row["Form Label"], page])

        return new_toc_by_visit

    def create_bookmarks(self, crf_path: str, sds_path: str, output_path: str):
        """Create new bookmarks, based on Study Definion Specs

        Args:
            crf_path (str): Path to raw CRF. Expects level 1 bookmarks for each form. Format of the
                            Bookmark name: <Form_Label> (<Form_Name>). Form_Name and Form_Label has
                            to match SDS File
            sds_path (str): Path to Study Defintion Specs. Expects a xlsx file with sheet:
                            "Schedule - Grid"
            output_path (str): Path to create the new CRF with bookmarks
        """

        # open files
        input_crf = pymupdf.open(crf_path)
        sds = pd.read_excel(sds_path, sheet_name="Schedule - Grid", header=1, engine="openpyxl")

        sds.columns = ["Form Label", "Form Name", *sds.columns[2:].to_list()]
        # get all visits in the trail
        visit_labels = sds.columns.tolist()[2:]

        # get original toc
        toc_input = input_crf.get_toc(simple=True)

        input_bookmarks_dict = self.toc_to_bookmark_dict(toc_input)

        # create new bookmarks
        new_toc_by_form = self.create_bookmarks_form(sds, input_bookmarks_dict, visit_labels)
        new_toc_by_visit = self.create_bookmarks_visit(sds, input_bookmarks_dict, visit_labels)
        new_toc = new_toc_by_form + new_toc_by_visit

        # write new toc to file
        input_crf.set_toc(new_toc)

        # save new CRF
        input_crf.save(output_path)
