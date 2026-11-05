# goldpan

The analysis library of the NSDF-Data project, for pulse data from SuperCDMS-type detectors and anything else that has pulses plus the quantities computed from them: an immutable container of one detector's events (`Events`), adapters that read and write the file formats, the pulse quantities, cuts and filters, the dataset definition file and the reader of the detector registry.

Install it with `pip install goldpan`, and the extras you need: `goldpan[archive]` (HDF5), `goldpan[parquet]` (the native format), `goldpan[root]` (RQs in ROOT files), `goldpan[midas]` (MIDAS files). The code is at <https://github.com/villano-lab/goldpan>; its companion for reducing whole datasets is [goldsluice](https://villano-lab.github.io/goldsluice/).

Nothing about a readout is assumed: the sample period, the baseline window and every algorithm parameter are written down by the user, in a preset, in code or in the dataset definition file.

```{toctree}
:maxdepth: 2
:hidden:

concepts
guides
reference/index
```

## Where to start

| You want to | Read |
|---|---|
| understand how the pieces fit | {doc}`concepts` |
| write an adapter, define a dataset | {doc}`guides` |
| look up a function, class or module | {doc}`reference/index` |

This documentation is generated from the code and the pages in `docs/` of the repository. The project front page, the student guides and the notes are at <https://villano-lab.github.io/NSDF-Data/>.
