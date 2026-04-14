"""Core Idea->
Maintain a separate waiting queue per language 
and a pool of free agents per language. 

free_agents_by_lang[Language]  -> agents available for that language
waiting_calls_by_lang[Language] -> queued customers
"""

from enum import Enum
from collections import deque, defaultdict
import time
import heapq

class Language(Enum):
    HINDI = "hindi"
    KANNADA = "kannada"
    TAMIL = "tamil"
    TELUGU = "telugu"
    ENGLISH = "english"

class CustomerTier(Enum):
    LUXURY = 0
    FREE = 1


class CustomerCall:
    def __init__(self, call_id, language, tier: CustomerTier):
        self.call_id = call_id
        self.language = language
        self.tier = tier
        self.created_at = time.time()

    # heap needs comparator
    def priority_key(self):
        return (self.tier.value, self.created_at)

    def __repr__(self):
        return f"<Call {self.call_id} {self.tier.name} {self.language.value}>"


class Agent:
    def __init__(self, agent_id: str, name: str, languages: list[Language]):
        if len(languages) != 2:
            raise ValueError("Agent must know exactly 2 languages")

        self.agent_id = agent_id
        self.name = name
        self.languages = languages
        self.is_busy = False

    def __repr__(self):
        langs = ",".join([l.value for l in self.languages])
        return f"<Agent {self.name} [{langs}]>"



class AgentDirectory:
    def __init__(self):
        # language -> queue of agents
        self.free_agents_by_lang = defaultdict(deque)

    def login(self, agent: Agent):
        # agent becomes available for both languages
        agent.is_busy = False
        for lang in agent.languages:
            self.free_agents_by_lang[lang].append(agent)

    def mark_free(self, agent: Agent):
        agent.is_busy = False
        for lang in agent.languages:
            self.free_agents_by_lang[lang].append(agent)

    def get_agent_for(self, language: Language):
        queue = self.free_agents_by_lang[language]
        # skip busy agents
        while queue:
            candidate = queue.popleft()
            if not candidate.is_busy:
                return candidate
        return None


class PriorityCallQueues:
    def __init__(self):
        # language -> min heap
        self.waiting = defaultdict(list)

    def add(self, call: CustomerCall):
        heapq.heappush(self.waiting[call.language], (call.priority_key(), call))

    def next_call(self, language):
        heap = self.waiting[language]
        if heap:
            _, call = heapq.heappop(heap)
            return call
        return None

class CallRouter:
    def __init__(self, directory: AgentDirectory, queues: PriorityCallQueues):
        self.directory = directory
        self.queues = queues

    # new incoming call
    def handle_incoming_call(self, call):
        agent = self.directory.get_agent_for(call.language)
        if agent:
            self._connect(call, agent)
        else:
            print(f"Queued {call}")
            self.queues.add(call)

    # when agent finishes a call
    def handle_agent_available(self, agent: Agent):
        # try both languages agent knows
        for lang in agent.languages:
            waiting = self.queues.next_call(lang)
            if waiting:
                self._connect(waiting, agent)
                return
        # no waiting calls
        self.directory.mark_free(agent)

    def _connect(self, call: CustomerCall, agent: Agent):
        agent.is_busy = True
        print(f"Connected {call} -> {agent}")

def is_sla_violated(call):
    now = time.time()
    wait = now - call.created_at
    if call.tier == CustomerTier.LUXURY:
        return wait > 10
    else:
        return wait > 60

if __name__ == "__main__":
    directory = AgentDirectory()
    queues = PriorityCallQueues()
    router = CallRouter(directory, queues)

    # Agents (each knows 2 languages)
    rohit = Agent("A1", "Rohit", [Language.HINDI, Language.ENGLISH])
    vijay = Agent("A2", "Vijay", [Language.KANNADA, Language.TAMIL])
    anita = Agent("A3", "Anita", [Language.TELUGU, Language.HINDI])

    directory.login(rohit)
    directory.login(vijay)
    directory.login(anita)

    # Incoming calls
    router.handle_incoming_call(
        CustomerCall("C101", Language.HINDI, CustomerTier.FREE)
    )

    router.handle_incoming_call(
        CustomerCall("C102", Language.HINDI, CustomerTier.LUXURY)
    )
    router.handle_incoming_call(CustomerCall("C2", Language.TAMIL))
    router.handle_incoming_call(CustomerCall("C3", Language.KANNADA))
    router.handle_incoming_call(CustomerCall("C4", Language.TELUGU))

    # simulate agent becomes free
    router.handle_agent_available(rohit)



"""Horizontal Scaling
CallRouter can be stateless
Queues and agent state stored in:Redis,In-memory data grid
Telephony events handled via message queues (Kafka / PubSub)"""