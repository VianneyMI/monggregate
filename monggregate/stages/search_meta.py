"""xxx"""

from monggregate.stages.search import Search


class SearchMeta(Search):
    """xxxx"""

    @property
    def statement(self) -> dict[str, dict]:
    
        config = {
                "index":self.index,
                "highlight":self.highlight,
                "count":self.count,
                "returnStoredSource":self.return_stored_source,
                "scoreDetails":self.score_details
            }
        
        method:dict[str, dict] = self.collector or self.operator

        config.update(method)

        _statement = {
            "$searchMeta":config
        }
     
        return self.resolve(_statement)
    