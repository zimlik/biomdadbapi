# -*- encoding: utf-8 -*-
# @File: crud.py

from sqlmodel import Session, select, and_, or_
from .models import (Compound2cid, Cid2ssimcid, Disease2doid, Doid2gene,
                     Protein2stringid, PPI, Pnode, CPI, CCI, Cnode,
                     TargetProtein)
from .utilities import row_to_dict
from .database import engine
import re

async def sel_compound2cid(md5sum: list[str]):
    with Session(engine) as session:
        stmt = select(Compound2cid).where(Compound2cid.md5sum.in_(md5sum))
        md5sum2cid = session.exec(stmt).all()
    if (len(md5sum2cid) == 0):
        res = None
    else:
        md5sum2cid = row_to_dict(Compound2cid, md5sum2cid)
        res = {'md5sum2cid': md5sum2cid}
    return res

async def sel_cid2info(cid: list[str]):
    with Session(engine) as session:
        stmt = select(Cnode).where(Cnode.id.in_(cid))
        cnodes = session.exec(stmt).all()
    if (len(cnodes) == 0):
        res = None
    else:
        cnodes = row_to_dict(Cnode, cnodes)
        res = {'cnodes': cnodes}
    return res

async def sel_stringid2info(stringid: list[str]):
    with Session(engine) as session:
        stmt = select(Pnode).where(Pnode.id.in_(stringid))
        pnodes = session.exec(stmt).all()
    if (len(pnodes) == 0):
        res = None
    else:
        pnodes = row_to_dict(Pnode, pnodes)
        res = {'pnodes': pnodes}
    return res

async def sel_cid2ssimcid(cid: list[str]):
    with Session(engine) as session:
        stmt = select(Cid2ssimcid).where(Cid2ssimcid.cid.in_(cid))
        cid2ssimcid = session.exec(stmt).all()
    if (len(cid2ssimcid) == 0):
        res = None
    else:
        cid2ssimcid = row_to_dict(Cid2ssimcid, cid2ssimcid)
        ssimcid = [row['ssimcid'].split(',') for row in cid2ssimcid]
        ssimcid = [item for item_list in ssimcid for item in item_list]
        ssimcid = list(set(ssimcid))
        with Session(engine) as session:
            stmt2 = select(Cnode).where(Cnode.id.in_(ssimcid))
            cnodes = session.exec(stmt2).all()
        cnodes = row_to_dict(Cnode, cnodes)
        res = {'cid2ssimcid': cid2ssimcid, 'cnodes': cnodes}
    return res

async def sel_disease2doid(disease: str, fixed: bool):
    if re.match(r'^DOID:[0-9]+$', disease):
        with Session(engine) as session:
            stmt = (select(Disease2doid).
                    where(Disease2doid.doid == disease))
            d2doid = session.exec(stmt).all()
    else:
        if fixed:
            with Session(engine) as session:
                stmt = (select(Disease2doid).
                        where(Disease2doid.disease == disease))
                d2doid = session.exec(stmt).all()
        else:
            patt = f'%{disease}%'
            with Session(engine) as session:
                stmt = (select(Disease2doid).
                        where(Disease2doid.disease.like(patt)))
                d2doid = session.exec(stmt).all()
    if (len(d2doid) == 0):
        res = None
    else:
        d2doid = row_to_dict(Disease2doid, d2doid)
        res = {'d2doid': d2doid}
    return res

async def sel_doid2gene(doid: str):
    with Session(engine) as session:
        stmt = select(Doid2gene).where(Doid2gene.doid == doid)
        doid2gene = session.exec(stmt).all()
    if (len(doid2gene) == 0):
        res = None
    else:
        doid2gene = row_to_dict(Doid2gene, doid2gene)
        res = {'doid2gene': doid2gene}
    return res

async def sel_protein2stringid(protein: list[str]):
    with Session(engine) as session:
        stmt = (select(Protein2stringid).
                where(Protein2stringid.protein.in_(protein)))
        p2string = session.exec(stmt).all()
    if (len(p2string) == 0):
        res = None
    else:
        p2string = row_to_dict(Protein2stringid, p2string)
        stringid = [row['id'] for row in p2string]
        stringid = list(set(stringid))
        with Session(engine) as session:
            stmt2 = select(Pnode).where(Pnode.id.in_(stringid))
            pnodes = session.exec(stmt2).all()
        pnodes = row_to_dict(Pnode, pnodes)
        res = {'p2string': p2string, 'pnodes': pnodes}
    return res

async def sel_string_ppi(stringid: list[str], score: int):
    with Session(engine) as session:
        stmt1 = (select(PPI).
                where(and_(or_(PPI.node1.in_(stringid),
                               PPI.node2.in_(stringid)),
                           PPI.score >= score)))
        edges1 = session.exec(stmt1).all()
    if (len(edges1) == 0):
        res = None
    else:
        edges1 = row_to_dict(PPI, edges1)
        spid1 = [row['node1'] for row in edges1]
        spid2 = [row['node2'] for row in edges1]
        all_spid = list(set(spid1 + spid2))
        new_spid = [sid for sid in all_spid if sid not in stringid]
        if (len(new_spid) < 2):
            edges = edges1
        else:
            with Session(engine) as session:
                stmt2 = (select(PPI).
                         where(and_(PPI.node1.in_(new_spid),
                                    PPI.node2.in_(new_spid),
                                    PPI.score >= score)))
                edges2 = session.exec(stmt2).all()
            edges2 = row_to_dict(PPI, edges2)
            edges = edges1 + edges2
        with Session(engine) as session:
            stmt3 = (select(Pnode).
                     where(Pnode.id.in_(all_spid)))
            nodes = session.exec(stmt3).all()
        nodes = row_to_dict(Pnode, nodes)
        res = {'edges': edges, 'nodes': nodes}
    return res

async def sel_tgtp_cpi(cid: list[str], score: int):
    with Session(engine) as session:
        stmt1 = (select(TargetProtein).
                 where(and_(TargetProtein.node1.in_(cid),
                            TargetProtein.score >= score)))
        tgtp_cpi = session.exec(stmt1).all()
    if (len(tgtp_cpi) == 0):
        res = None
    else:
        tgtp_cpi = row_to_dict(TargetProtein, tgtp_cpi)
        stringid = [row['node2'] for row in tgtp_cpi]
        with Session(engine) as session:
            stmt2 = select(Pnode).where(Pnode.id.in_(stringid))
            tgtp_pnode = session.exec(stmt2).all()
        tgtp_pnode = row_to_dict(Pnode, tgtp_pnode)
        res = {'tgtp_cpi': tgtp_cpi, 'tgtp_pnode': tgtp_pnode}
    return res


async def sel_stitch_cpi(cid: list[str], score: int):
    with Session(engine) as session:
        stmt1 = (select(CPI).
                 where(and_(or_(CPI.node1.in_(cid),
                                CPI.node2.in_(cid)),
                            CPI.score >= score)))
        cpi = session.exec(stmt1).all()
    if (len(cpi) == 0):
        res = None
    else:
        cpi = row_to_dict(CPI, cpi)
        scid = [row['node1'] for row in cpi]
        scid = list(set(scid))
        spid = [row['node2'] for row in cpi]
        spid = list(set(spid))
        if (len(scid) < 2):
            cci = None
        else:
            with Session(engine) as session:
                stmt2 = (select(CCI).
                        where(and_(CCI.node1.in_(scid),
                                   CCI.node2.in_(scid),
                                   CCI.score >= score)))
                cci = session.exec(stmt2).all()
            cci = row_to_dict(CCI, cci)
        if (len(spid) < 2):
            ppi = None
        else:
            with Session(engine) as session:
                stmt3 = (select(PPI).
                        where(and_(PPI.node1.in_(spid),
                                   PPI.node2.in_(spid),
                                   PPI.score >= score)))
                ppi = session.exec(stmt3).all()
            ppi = row_to_dict(PPI, ppi)
        edges = {'cpi': cpi, 'cci': cci, 'ppi': ppi}

        with Session(engine) as session:
            stmt4 = select(Cnode).where(Cnode.id.in_(scid))
            cnodes = session.exec(stmt4).all()
        cnodes = row_to_dict(Cnode, cnodes)
        with Session(engine) as session:
            stmt5 = select(Pnode).where(Pnode.id.in_(spid))
            pnodes = session.exec(stmt5).all()
        pnodes = row_to_dict(Pnode, pnodes)
        nodes = {'cnodes': cnodes, 'pnodes': pnodes}
        res = {'edges': edges, 'nodes': nodes}
    return res