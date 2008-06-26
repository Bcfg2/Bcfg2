'''Minestruct Admin Mode'''
import Bcfg2.Server.Admin
import lxml.etree

class Minestruct(Bcfg2.Server.Admin.Mode):
    '''Pull extra entries out of statistics'''
    __shorthelp__ = 'bcfg2-admin minestruct <client> [-f file-name] [-g groups]'
    __longhelp__ = __shorthelp__ + '\n\tExtract extra entry lists from statistics'

    def __init__(self, cfile):
        Bcfg2.Server.Admin.Mode.__init__(self, cfile)

    def __call__(self, args):
        Bcfg2.Server.Admin.Mode.__call__(self, args)
        if len(args) == 0:
            self.errExit("No hostname specified (see bcfg2-admin minestruct -h for help)")
        if "-h" in args:
            print "Usage:"
            print self.__shorthelp__
            raise SystemExit(1)
        write_to_file = False
        file_arg = False
        output_file = None
        client = None
        groups_arg = False
        groups = []
        for arg in args:
            if arg == "-f":
                file_arg = True
                groups_arg = False
                continue
            elif arg == "-g":
                groups_arg = True
                file_arg = False
                continue                           
            elif file_arg == True:
                output_file = arg
                file_arg = False
                write_to_file = True
                continue
            elif groups_arg == True:
                groups.append(arg)
                continue
            else:
                client = arg
        stats = self.load_stats(client)
        if len(stats.getchildren()) == 2:
            # client is dirty
            current = [ent for ent in stats.getchildren() if ent.get('state') == 'dirty'][0]
        else:
            current = stats.getchildren()[0]
        extra = current.find('Extra').getchildren()
        root = lxml.etree.Element("Base")
        self.log.info("Found %d extra entries" % (len(extra)))
        if len(groups) == 0:
            for entry in extra:
                self.log.info("%s: %s" % (entry.tag, entry.get('name')))
                root.append(lxml.etree.Element(entry.tag, name=entry.get('name')))
        else:
            groups_root = lxml.etree.Element("Group", name=groups[0])
            root.append(groups_root) 
            for i in range (1, len(groups)):
                temp = lxml.etree.Element("Group", name=groups[i])
                groups_root.append(temp)
                groups_root = temp
            for entry in extra:
                self.log.info("%s: %s" % (entry.tag, entry.get('name')))
                groups_root.append(lxml.etree.Element(entry.tag, name=entry.get('name')))
        tree = lxml.etree.ElementTree(root)
        if write_to_file == True:
            try:
                f = open(output_file, 'w')
            except IOError:
                self.log.info("Failed to write to file: %s" % (output_file))
                raise SystemExit(1)
            tree.write(f)

