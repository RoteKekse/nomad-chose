#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from baseclasses import (
    BaseProcess, BaseMeasurement, LayerDeposition, Batch
)


from baseclasses.experimental_plan import ExperimentalPlan
from baseclasses.material_processes_misc import (
    Cleaning,
    SolutionCleaning,
    PlasmaCleaning,
    UVCleaning,
    LaserScribing,
    Storage)
from baseclasses.solar_energy import (
    StandardSampleSolarCell, SolarCellProperties,
    Substrate,
    JVMeasurement,
    PLMeasurement,
    UVvisMeasurement,
    EQEMeasurement,
    SolcarCellSample, BasicSampleWithID,
    MPPTracking
)
from baseclasses.solution import Solution, SolutionChemical, SolutionPreparationStandard
from baseclasses.vapour_based_deposition import (
    Evaporations, Evaporation,
    AtomicLayerDeposition,
    Sputtering)
from baseclasses.wet_chemical_deposition import (
    SpinCoating,
    SlotDieCoating, DipCoating,
    LP50InkjetPrinting,
    SprayPyrolysis,
    WetChemicalDeposition)
from nomad.datamodel.data import EntryData
from nomad.datamodel.results import Results, Properties, Material, ELN
# from nomad.units import ureg
from nomad.metainfo import (
    Package,
    Quantity,
    SubSection,
    Section)

m_package0 = Package(name='Chose')


# %% ####################### Entities

class Chose_ExperimentalPlan(ExperimentalPlan, EntryData):
    m_def = Section(
        a_eln=dict(hide=['users'],
                   properties=dict(
                       order=[
                           "name",
                           "standard_plan",
                           "load_standard_processes",
                           "create_samples_and_processes",
                           "number_of_substrates",
                           "substrates_per_subbatch",
                           "lab_id"
                       ])),
        a_template=dict(institute="HZB_Chose"))

    solar_cell_properties = SubSection(
        section_def=SolarCellProperties)

    def normalize(self, archive, logger):
        super(Chose_ExperimentalPlan, self).normalize(archive, logger)

        from baseclasses.helper.execute_solar_sample_plan import execute_solar_sample_plan
        execute_solar_sample_plan(self, archive, Chose_Sample, Chose_Batch, logger)

        # actual normalization!!
        archive.results = Results()
        archive.results.properties = Properties()
        archive.results.material = Material()
        archive.results.eln = ELN()
        archive.results.eln.sections = ["Chose_ExperimentalPlan"]


class Chose_StandardSample(StandardSampleSolarCell, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['users'],
            properties=dict(
                order=[
                    "name",
                    "architecture",
                    "substrate",
                    "processes",
                    "lab_id"
                ])))


class Chose_Substrate(Substrate, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users', 'components', 'elemental_composition'],
            properties=dict(
                order=[
                    "name",
                    "substrate",
                    "conducting_material",
                    "solar_cell_area",
                    "pixel_area",
                    "number_of_pixels"])))


class ChoseSolutionChemical(SolutionChemical):
    m_def = Section(label_quantity='name',  a_eln=dict(
        hide=['chemical']))


class Chose_Solution(Solution, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'users', 'components', 'elemental_composition', "method", "temperature", "time", "speed",
                "solvent_ratio", "washing"],
            properties=dict(
                order=[
                    "name",
                    "datetime",
                    "lab_id",
                    "description", "preparation", "solute", "solvent", "other_solution", "additive", "storage"
                ],
            )),
        a_template=dict(
            temperature=45,
            time=15,
            method='Shaker'))

    preparation = SubSection(section_def=SolutionPreparationStandard)
    solute = SubSection(section_def=ChoseSolutionChemical, repeats=True)
    additive = SubSection(section_def=ChoseSolutionChemical, repeats=True)
    solvent = SubSection(section_def=ChoseSolutionChemical, repeats=True)


class Chose_Sample(SolcarCellSample, EntryData):
    m_def = Section(
        a_eln=dict(hide=['users', 'components', 'elemental_composition'], properties=dict(
            order=["name", "substrate", "architecture"])),
        a_template=dict(institute="HZB_Chose"),
        label_quantity='sample_id'
    )


class Chose_BasicSample(BasicSampleWithID, EntryData):
    m_def = Section(
        a_eln=dict(hide=['users', 'components', 'elemental_composition']),
        a_template=dict(institute="HZB_Chose"),
        label_quantity='sample_id'
    )


class Chose_Batch(Batch, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['users', 'samples'],
            properties=dict(
                order=[
                    "name",
                    "export_batch_ids",
                    "csv_export_file"])))


# %% ####################### Cleaning
class Chose_Cleaning(Cleaning, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime", "previous_process",
                    "batch",
                    "samples"])))

    location = Quantity(
        type=str,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['Chose', 'IRIS Printerlab', 'IRIS Preparationlab'])
        ))

    cleaning = SubSection(
        section_def=SolutionCleaning, repeats=True)

    cleaning_uv = SubSection(
        section_def=UVCleaning, repeats=True)

    cleaning_plasma = SubSection(
        section_def=PlasmaCleaning, repeats=True)


# %% ##################### Layer Deposition
class Chose_SprayPyrolysis(SprayPyrolysis, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime", "previous_process",
                    "batch",
                    "samples",
                    "solution",
                    "layer",
                    "properties",
                    "quenching",
                    "annealing"])))

    location = Quantity(
        type=str,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['Chose HTFumeHood'])
        ))


# %% ### Printing


class Chose_Inkjet_Printing(
        LP50InkjetPrinting, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "recipe_used", "print_head_used",
                    "datetime", "previous_process",
                    "batch",
                    "samples",
                    "solution",
                    "layer",
                    "properties",
                    "print_head_path",
                    "nozzle_voltage_profile",
                    "quenching",
                    "annealing"])),
        a_template=dict(
            layer_type="Absorber Layer",
        ))

    location = Quantity(
        type=str,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['IRIS HZBGloveBoxes Pero3Inkjet'])
        ))


# %% ### Spin Coating
class Chose_SpinCoating(SpinCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results', 'recipe'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "recipe"
                    "datetime", "previous_process",
                    "batch",
                    "samples",
                    "solution",
                    "layer",
                    "quenching",
                    "annealing"])),
        a_template=dict(
            layer_type="Absorber Layer",
        ))

    location = Quantity(
        type=str,
        a_eln=dict(
            component='EnumEditQuantity',
            props=dict(
                suggestions=['Chose HyFlowBox', 'Chose HyPeroSpin', 'Chose HySpin', 'Chose ProtoVap',
                             'IRIS HZBGloveBoxes Pero2Spincoater'])
        ))


# %% ### Dip Coating


class Chose_DipCoating(DipCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime",
                    "batch",
                    "samples",
                    "solution",
                    "layer",
                    "quenching",
                    "annealing"])),
        a_template=dict(
            layer_type="Absorber Layer",
        ))


# %% ### Slot Die Coating


class Chose_SlotDieCoating(SlotDieCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'author',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime", "previous_process",
                    "batch",
                    "samples",
                    "solution",
                    "layer",
                    "properties",
                    "quenching",
                    "annealing"
                ])),
        a_template=dict(
            layer_type="Absorber Layer"))


# %% ### Sputterring
class Chose_Sputtering(
        Sputtering, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime",
                    "batch",
                    "samples", "layer"])))


# %% ### AtomicLayerDepositio
class Chose_AtomicLayerDeposition(
        AtomicLayerDeposition, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime",
                    "batch",
                    "samples", "layer"])))


# %% ### Evaporation

class ChoseEvaporation(Evaporation):
    m_def = Section(label_quantity='name',  a_eln=dict(
        hide=['chemical']))


class Chose_Evaporation(
        Evaporations, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results', "organic_evaporation", "inorganic_evaporation",
                "perovskite_evaporation"],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime",
                    "batch",
                    "samples", "layer"])))

    properties = SubSection(
        section_def=ChoseEvaporation)


# %% ## Laser Scribing
class Chose_LaserScribing(LaserScribing, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime",
                    "batch",
                    "samples"])))


# %% ## Storage


class Chose_Storage(Storage, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name", "location",
                    "present",
                    "datetime", "previous_process",
                    "batch",
                    "samples"])))


# %%####################################### Measurements


class Chose_JVmeasurement(JVMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id', 'solution',
                'users',
                'author',
                'certified_values',
                'certification_institute',
                'end_time', 'steps', 'instruments', 'results',
            ],
            properties=dict(
                order=[
                    "name",
                    "data_file",
                    "active_area",
                    "intensity",
                    "integration_time",
                    "settling_time",
                    "averaging",
                    "compliance",
                    "samples"])),
        a_plot=[
            {
                'x': 'jv_curve/:/voltage',
                'y': 'jv_curve/:/current_density',
                'layout': {
                    "showlegend": True,
                    'yaxis': {
                        "fixedrange": False},
                    'xaxis': {
                        "fixedrange": False}},
            }])

    def normalize(self, archive, logger):
        if self.data_file:
            # todo detect file format
            from baseclasses.helper.utilities import get_encoding
            with archive.m_context.raw_file(self.data_file, "br") as f:
                encoding = get_encoding(f)

            with archive.m_context.raw_file(self.data_file, encoding=encoding) as f:
                from .jv_parser import get_jv_data
                from baseclasses.helper.archive_builder.jv_archive import get_jv_archive

                jv_dict = get_jv_data(f.name, encoding)
                get_jv_archive(jv_dict, self.data_file, self)

        super(Chose_JVmeasurement, self).normalize(archive, logger)


class Chose_MPPTracking(MPPTracking, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time',  'steps', 'instruments', 'results', ],
            properties=dict(
                order=[
                    "name",
                    "data_file",
                    "samples"])),
        a_plot=[
            {
                'x': 'time',
                'y': ['efficiency', 'voltage'],
                'layout': {
                    "showlegend": True,
                    'yaxis': {
                        "fixedrange": False},
                    'xaxis': {
                        "fixedrange": False}},
            }])

    def normalize(self, archive, logger):
        if self.data_file:
            from baseclasses.helper.utilities import get_encoding
            with archive.m_context.raw_file(self.data_file, "br") as f:
                encoding = get_encoding(f)

            with archive.m_context.raw_file(self.data_file, encoding=encoding) as f:
                from .mpp_parser import get_mpp_data, get_mpp_archive
                mpp_dict, data = get_mpp_data(f.name, encoding)
                get_mpp_archive(mpp_dict, data, self)
        super(Chose_MPPTracking, self).normalize(archive, logger)


class Chose_EQEmeasurement(EQEMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id', 'solution',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "data_file",
                    "samples"])),
        a_plot=[
            {
                'x': 'eqe_data/:/photon_energy_array',
                'y': 'eqe_data/:/eqe_array',
                'layout': {
                    "showlegend": True,
                    'yaxis': {
                        "fixedrange": False},
                    'xaxis': {
                        "fixedrange": False}},
            }])


class Chose_PLmeasurement(PLMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "data_file",
                    "samples", "solution"])),
        a_plot=[
            {
                'x': 'data/wavelength',
                'y': 'data/intensity',
                'layout': {
                    "showlegend": True,
                    'yaxis': {
                        "fixedrange": False},
                    'xaxis': {
                        "fixedrange": False}},
            }])

    def normalize(self, archive, logger):

        super(Chose_PLmeasurement, self).normalize(archive, logger)


class Chose_UVvismeasurement(UVvisMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "data_file",
                    "samples", "solution"])))

    def normalize(self, archive, logger):

        super(Chose_UVvismeasurement,
              self).normalize(archive, logger)


# %%####################################### Generic Entries


class Chose_Process(BaseProcess, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "present",
                    "data_file",
                    "batch",
                    "samples"])))

    data_file = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'))


class Chose_WetChemicalDepoistion(WetChemicalDeposition, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "present",
                    "datetime", "previous_process",
                    "batch",
                    "samples",
                    "solution",
                    "layer",
                    "quenching",
                    "annealing"])))

    data_file = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'))


class Chose_Deposition(LayerDeposition, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "present",
                    "datetime", "previous_process",
                    "batch",
                    "samples",
                    "layer"
                ])))

    data_file = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'))


class Chose_Measurement(BaseMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    "name",
                    "data_file",
                    "samples", "solution"])))

    data_file = Quantity(
        type=str,
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'))
