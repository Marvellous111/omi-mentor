import asyncio
from typing import Dict, List

class OneQueue:
  def __init__(self):
    self.queue = asyncio.Queue(maxsize=1)
    
  async def fill_queue_one_item(self, item: Dict):
    """Given an item at all times then the queue will and must only have one item in it

    Args:
        item (Dict): An item that is a string or perhaps a dictionary
    """
    if self.queue.qsize() > 0:
      await self.queue.get()
      await self.queue.put(item)
    else:
      await self.queue.put(item)
    
  async def fill_queue_multiple_items(self, items: List, order:str):
    """Given multiple items the queue will only contain just one item and depending on the order
    of items it will be either the first item in the items or the last one remaining in the queue

    Args:
        items (List): list of items
        order (str): order of item you want in the queue, 'first' for first item or 'last; for last item to be in the queue
    """
    
    if self.queue.qsize() > 0:
      await self.queue.get()
      if order == 'first':
        await self.queue.put(items[0])
      elif order == 'last':
        await self.queue.put(items[len(items)-1])
    else:
      if order == 'first':
        await self.queue.put(items[0])
      elif order == 'last':
        await self.queue.put(items[len(items)-1])
        
  async def get_queue_list(self):
    """Get the self.queue object for use

    Returns:
        _type_: asyncio.queue
    """
    return await self.queue