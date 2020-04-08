from AeroelasticAnalysis import AeroelasticAnalysis
from AeroelasticPanels import SuperAeroPanel5
from AeroelasticPostProcessing import plot_flutter_data, plot_critical_flutter_data, export_flutter_data, read_f06
from pyNastran.utils.nastran_utils import run_nastran
from femap import Femap
import os

if __name__ == '__main__':
    base_path = r'C:\Users\Victor\PycharmProjects\aero-5-mesh-gen'
    input_file = os.path.join(base_path, 'input-model.bdf')
    output_file = os.path.join(base_path, 'output-model.bdf')
    nastran_exe = r'D:\Programs\MSC.Software\NaPa_SE\2019fp1\Nastran\bin\nast20191.exe'

    analysis = AeroelasticAnalysis()
    femap = Femap()
    femap.export_bdf_model(input_file)
    analysis.import_from_bdf(input_file)
    spanel = SuperAeroPanel5(femap)
    spanel.init_from_femap()

    analysis.add_superpanel(spanel)
    analysis.create_subcase(1, os.path.join(base_path, r'analysis.yml'))
    analysis.write_cards(1)
    analysis.export_to_bdf(output_file)

    run_nastran(output_file, nastran_cmd=nastran_exe, keywords=['old=no'])

    modes, critical_modes, flutter = read_f06(output_file.replace('.bdf', '.f06'), analysis.subcases[1])
    plot_flutter_data(modes, analysis.subcases[1])
    plot_critical_flutter_data(critical_modes, analysis.subcases[1])
    export_flutter_data(modes, critical_modes, flutter, analysis.subcases[1], os.path.join(base_path, 'test.xlsx'))