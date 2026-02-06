#!/usr/bin/env python3
import argparse
from datetime import date
from devprod.db import DB
import csv
from pathlib import Path

def iso_date(d: str) -> str:
    if d in (None, '', 'today'):
        return date.today().isoformat()
    return d

def cmd_init(args):
    db = DB(args.db)
    print(f"Initialized DB at: {db.path}")
    db.close()

def cmd_log(args):
    db = DB(args.db)
    d = iso_date(args.date)
    rid = db.add_entry(d, args.project, args.hours, args.notes or '')
    print(f"Logged entry id={rid} date={d} project={args.project} hours={args.hours}")
    db.close()

def cmd_list(args):
    db = DB(args.db)
    d = iso_date(args.date) if args.date else None
    rows = db.list_entries(start=d, end=None) if d else db.list_entries()
    for r in rows:
        print(f"{r['id']} | {r['date']} | {r['project']} | {r['hours']} | {r['notes']}")
    db.close()

def cmd_summary(args):
    db = DB(args.db)
    start = iso_date(args.date)
    end = args.end
    rows = db.summary(start, end)
    total = db.total_hours(start, end)
    print(f"Summary {start}{(' to '+end) if end else ''}")
    for r in rows:
        print(f"- {r['project']}: {r['total']} hours")
    print(f"Total: {total} hours")
    db.close()

def cmd_export(args):
    db = DB(args.db)
    rows = db.list_entries(start=args.date) if args.date else db.list_entries()
    out = Path(args.out).resolve() if args.out else Path('devprod_export.csv').resolve()
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id','date','project','hours','notes','created_at'])
        for r in rows:
            w.writerow([r['id'], r['date'], r['project'], r['hours'], r['notes'], r['created_at']])
    print(f"Exported {len(rows)} rows to {out}")
    db.close()

def build_parser():
    p = argparse.ArgumentParser(prog='devprod', description='Dev Productivity Tracker')
    p.add_argument('--db', help='Path to DB file (overrides default)')
    sp = p.add_subparsers(dest='cmd')

    p_init = sp.add_parser('init')
    p_init.set_defaults(func=cmd_init)

    p_log = sp.add_parser('log')
    p_log.add_argument('--project', required=True)
    p_log.add_argument('--hours', type=float, required=True)
    p_log.add_argument('--notes', default='')
    p_log.add_argument('--date', default='today')
    p_log.set_defaults(func=cmd_log)

    p_list = sp.add_parser('list')
    p_list.add_argument('--date', default=None, help='YYYY-MM-DD or "today"')
    p_list.set_defaults(func=cmd_list)

    p_sum = sp.add_parser('summary')
    p_sum.add_argument('--date', default='today')
    p_sum.add_argument('--end', default=None, help='End date for range (YYYY-MM-DD)')
    p_sum.set_defaults(func=cmd_summary)

    p_exp = sp.add_parser('export')
    p_exp.add_argument('--out', help='Output CSV path')
    p_exp.add_argument('--date', default=None)
    p_exp.set_defaults(func=cmd_export)

    return p

def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if not hasattr(args, 'func'):
        p.print_help()
        return 1
    return args.func(args)

if __name__ == '__main__':
    raise SystemExit(main())
