
import sys, hughml, test_appliance

def main(args=None):
    collections = []
    import test_hughml
    collections.append(test_hughml)
    if hughml.__with_libhughml__:
        import test_hughml_ext
        collections.append(test_hughml_ext)
    return test_appliance.run(collections, args)

if __name__ == '__main__':
    main()

