#!/usr/bin/env python2
import random
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "Neo4j"))
session = driver.session()
session.run("match (n) detach delete n")

# Create subnet nodes, which will act similarly to switches in a network.
# One device may have multiple subnets, these devices act similarly to routers.
subnets = ["public", "corporate", "enclave", "internet"]
for subnet in subnets:
    session.run("CREATE (a:Subnet {name: '" + subnet + "'})")

# Create the host nodes. These will connect to at least one of the above subnets.
# 1 in 10 hosts will connect to two subnets, acting as the router between them.
session.run(""" MATCH (b:Subnet {name: 'internet'})
                CREATE (a:Machine {name: 'entry', vuln: 'false'})-[:isIn]->(b)""")
session.run(""" MATCH (a:Machine {name: 'entry'})
                CREATE (a)-[:isIn]->(:Subnet {name: 'hackerNet'})""")

names = ["adelphi", "antares", "apollo", "archer", "armstrong", "bradbury", "cairo", "challenger", "chekov", "copernicus",
        "defiant", "discovery", "endeavour", "enterprise", "excelsior", "firebrand", "franklin", "ganymede", "gettysburg",
        "hathaway", "heart of gold", "hood", "lakota", "prometheus", "sarek", "stargaver", "tsiolkovsky", "ulysses", "voyager",
        "yorktown"]
for name in names:
    vuln = ("true" if (random.randint(0, 10) in range(0, 9)) else "false")
    subnet = subnets[random.randint(0, len(subnets)-1)]
    if(random.randint(0, 10) in range(4,7)): # chosen by fair dice roll. See 221.
        vuln = ("true" if (random.randint(0, 8) in range(0,6)) else "false")
        subnet2 = subnets[random.randint(0, len(subnets)-1)]
        session.run("CREATE (a:Machine {name: '" + name + "', vuln: '" + vuln + "'})")
        session.run("MATCH (a:Machine {name: '" + name + """'})
                     MATCH (b:Subnet {name: '""" + subnet + """'})
                     CREATE (a)-[:isIn]->(b)""")

        session.run("MATCH (a:Machine {name: '" + name + """'})
                     MATCH (b:Subnet {name: '""" + subnet2 + """'})
                     CREATE (a)-[:isIn]->(b)""")
    else:
        session.run("CREATE (a:Machine {name: '" + name + "', vuln: '" + vuln + "'})")
        session.run("MATCH (a:Machine {name: '" + name + """'})
                     MATCH (b:Subnet {name: '""" + subnet + """'})
                     CREATE (a)-[:isIn]->(b)""")

result = session.run("MATCH (a:Machine {name: '" + name + """'})
                     MATCH (b:Subnet {name: '""" + subnet + """'})
                RETURN a,b""")

result = session.run(""" MATCH (a:Machine)-[:isIn]->(:Subnet)<-[:isIn]-(b:Machine)
                WHERE (a.name <> b.name) AND (b.vuln = 'true')
                CREATE (a)-[:canAttack]->(b)
                RETURN a""")

session.close()
