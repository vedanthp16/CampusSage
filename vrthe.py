from typing import Optional, Text, Dict, List, Union

import rasa
from rasa.shared.core.domain import Domain
from rasa.shared.nlu.interpreter import RegexInterpreter
from rasa.shared.core.training_data.structures import StoryGraph
from rasa.shared.importers.importer import TrainingDataImporter
from rasa.shared.nlu.training_data.training_data import TrainingData


class MyImporter(TrainingDataImporter):
    """Example implementation of a custom importer component."""

    def __init__(
        self,
        config_file: Optional[Text] = None,
        domain_path: Optional[Text] = None,
        training_data_paths: Optional[Union[List[Text], Text]] = None,
        **kwargs: Dict
    ):
        """Constructor of your custom file importer.

        Args:
            config_file: Path to configuration file from command line arguments.
            domain_path: Path to domain file from command line arguments.
            training_data_paths: Path to training files from command line arguments.
            **kwargs: Extra parameters passed through configuration in configuration file.
        """

        pass

    def get_domain(self) -> Domain:
        path_to_domain_file = self._custom_get_domain_file()
        return Domain.load(path_to_domain_file)

    def _custom_get_domain_file(self) -> Text:
        pass

    def get_stories(
        self,
        interpreter: "NaturalLanguageInterpreter" = RegexInterpreter(),
        exclusion_percentage: Optional[int] = None,
    ) -> StoryGraph:
        from rasa.shared.core.training_data.story_reader.yaml_story_reader import (
            YAMLStoryReader,
        )

        path_to_stories = self._custom_get_story_file()
        return YAMLStoryReader.read_from_file(path_to_stories, self.get_domain())

    def _custom_get_story_file(self) -> Text:
        pass

    def get_config(self) -> Dict:
        path_to_config = self._custom_get_config_file()
        return rasa.utils.io.read_config_file(path_to_config)

    def _custom_get_config_file(self) -> Text:
        pass

    def get_nlu_data(self, language: Optional[Text] = "en") -> TrainingData:
        from rasa.shared.nlu.training_data import loading

        path_to_nlu_file = self._custom_get_nlu_file()
        return loading.load_data(path_to_nlu_file)

    def _custom_get_nlu_file(self) -> Text:
        pass