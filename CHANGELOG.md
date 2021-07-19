# Changelog

## [Unreleased](https://github.com/jonathan-s/django-sockpuppet/tree/HEAD)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.6.0...HEAD)

**Implemented enhancements:**

- CI for django 3.2 [\#127](https://github.com/jonathan-s/django-sockpuppet/pull/127) ([jonathan-s](https://github.com/jonathan-s))
- extract/const isProd [\#118](https://github.com/jonathan-s/django-sockpuppet/pull/118) ([nerdoc](https://github.com/nerdoc))
- camelCase/PascalCase correction of reflex scaffolding [\#87](https://github.com/jonathan-s/django-sockpuppet/pull/87) ([nerdoc](https://github.com/nerdoc))

**Fixed bugs:**

- Fixing running initial\_sockpuppet in windows [\#132](https://github.com/jonathan-s/django-sockpuppet/pull/132) ([ciag00](https://github.com/ciag00))
- Don't call get\_context\_data more than necessary [\#124](https://github.com/jonathan-s/django-sockpuppet/pull/124) ([jonathan-s](https://github.com/jonathan-s))

**Closed issues:**

- afterReflex, reflexSuccess, reflexError don't trigger if the element which "caused" the reflex isn't present on the page after the reflex.. [\#133](https://github.com/jonathan-s/django-sockpuppet/issues/133)
- Exception doesn't trigger [\#123](https://github.com/jonathan-s/django-sockpuppet/issues/123)
- Can't run `python manage.py initial_sockpuppet` on Windows [\#106](https://github.com/jonathan-s/django-sockpuppet/issues/106)
- Django message framework not usable from Reflex [\#101](https://github.com/jonathan-s/django-sockpuppet/issues/101)
- use black to format code [\#88](https://github.com/jonathan-s/django-sockpuppet/issues/88)
- scaffolding a reflex produces wrong class name when it contains a \_ [\#84](https://github.com/jonathan-s/django-sockpuppet/issues/84)
- Build Tools General Discussion [\#64](https://github.com/jonathan-s/django-sockpuppet/issues/64)
- Fix some issues to increase package score [\#33](https://github.com/jonathan-s/django-sockpuppet/issues/33)

**Merged pull requests:**

- Bump dependencies [\#126](https://github.com/jonathan-s/django-sockpuppet/pull/126) ([jonathan-s](https://github.com/jonathan-s))
- Make the code black [\#125](https://github.com/jonathan-s/django-sockpuppet/pull/125) ([jonathan-s](https://github.com/jonathan-s))
- Minor fix [\#121](https://github.com/jonathan-s/django-sockpuppet/pull/121) ([tanrax](https://github.com/tanrax))

## [0.6.0](https://github.com/jonathan-s/django-sockpuppet/tree/0.6.0) (2021-04-19)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.5.2...0.6.0)

**Implemented enhancements:**

- CSRF validator and documentation for security [\#110](https://github.com/jonathan-s/django-sockpuppet/pull/110) ([jonathan-s](https://github.com/jonathan-s))

**Fixed bugs:**

- Fix the omission of the stimulus\_reflex variable [\#108](https://github.com/jonathan-s/django-sockpuppet/pull/108) ([jonathan-s](https://github.com/jonathan-s))

**Closed issues:**

- context\['stimulus\_reflex'\] KeyError [\#107](https://github.com/jonathan-s/django-sockpuppet/issues/107)
- Authentication and security documentation [\#104](https://github.com/jonathan-s/django-sockpuppet/issues/104)
- Mistakes in documentation. [\#97](https://github.com/jonathan-s/django-sockpuppet/issues/97)
- add-project-script missing in \(dev\) dependencies? [\#80](https://github.com/jonathan-s/django-sockpuppet/issues/80)

**Merged pull requests:**

- Bump ssri from 6.0.1 to 6.0.2 [\#109](https://github.com/jonathan-s/django-sockpuppet/pull/109) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump y18n from 4.0.0 to 4.0.1 [\#105](https://github.com/jonathan-s/django-sockpuppet/pull/105) ([dependabot[bot]](https://github.com/apps/dependabot))
- Enable secure websocket for secure sites [\#102](https://github.com/jonathan-s/django-sockpuppet/pull/102) ([fmalina](https://github.com/fmalina))
- force npm install add-project-script [\#94](https://github.com/jonathan-s/django-sockpuppet/pull/94) ([nerdoc](https://github.com/nerdoc))

## [0.5.2](https://github.com/jonathan-s/django-sockpuppet/tree/0.5.2) (2021-02-15)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.5.1...0.5.2)

**Fixed bugs:**

- Fixed object not found error for detail view [\#95](https://github.com/jonathan-s/django-sockpuppet/pull/95) ([sampokuokkanen](https://github.com/sampokuokkanen))
- object\_list now works for ListView and similar views [\#93](https://github.com/jonathan-s/django-sockpuppet/pull/93) ([jonathan-s](https://github.com/jonathan-s))
- Spread operators necessary on variables passed to the view function. [\#91](https://github.com/jonathan-s/django-sockpuppet/pull/91) ([DamnedScholar](https://github.com/DamnedScholar))
- Separate linting from tests and fixes actioncable is rejected in Chrome [\#89](https://github.com/jonathan-s/django-sockpuppet/pull/89) ([jonathan-s](https://github.com/jonathan-s))

**Merged pull requests:**

- Ignore .vscode [\#85](https://github.com/jonathan-s/django-sockpuppet/pull/85) ([DamnedScholar](https://github.com/DamnedScholar))

## [0.5.1](https://github.com/jonathan-s/django-sockpuppet/tree/0.5.1) (2021-02-14)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.5.0...0.5.1)

**Closed issues:**

- Can't dispatch event back to the user using Channel [\#81](https://github.com/jonathan-s/django-sockpuppet/issues/81)
- Integration tests that should be created [\#21](https://github.com/jonathan-s/django-sockpuppet/issues/21)
- Triggering a 500 error won't give frontend notice that such an error happened [\#3](https://github.com/jonathan-s/django-sockpuppet/issues/3)

## [0.5.0](https://github.com/jonathan-s/django-sockpuppet/tree/0.5.0) (2021-01-16)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.4.2...0.5.0)

**Implemented enhancements:**

- Make it possible to use channels 3 and beyond [\#75](https://github.com/jonathan-s/django-sockpuppet/pull/75) ([kaozdl](https://github.com/kaozdl))
- Add changelog generator and changelog [\#73](https://github.com/jonathan-s/django-sockpuppet/pull/73) ([jonathan-s](https://github.com/jonathan-s))
- A reflex can access the context of the view it came from [\#72](https://github.com/jonathan-s/django-sockpuppet/pull/72) ([jonathan-s](https://github.com/jonathan-s))

**Fixed bugs:**

- Bug fix: Better recovery when a Reflex isn't found. [\#68](https://github.com/jonathan-s/django-sockpuppet/pull/68) ([DamnedScholar](https://github.com/DamnedScholar))
- Proper error logging for frontend and backend [\#74](https://github.com/jonathan-s/django-sockpuppet/pull/74) ([jonathan-s](https://github.com/jonathan-s))
- Fix sourcemap url [\#71](https://github.com/jonathan-s/django-sockpuppet/pull/71) ([jonathan-s](https://github.com/jonathan-s))
- Closing socket on page reload [\#69](https://github.com/jonathan-s/django-sockpuppet/pull/69) ([jonathan-s](https://github.com/jonathan-s))

**Closed issues:**

- More helpful error message when not finding reflex.  [\#52](https://github.com/jonathan-s/django-sockpuppet/issues/52)
- Channels 3.0 Released \> Incompatibility [\#36](https://github.com/jonathan-s/django-sockpuppet/issues/36)
- Look over the webpack config that we generate [\#31](https://github.com/jonathan-s/django-sockpuppet/issues/31)

**Merged pull requests:**

- Out of band example [\#78](https://github.com/jonathan-s/django-sockpuppet/pull/78) ([jonathan-s](https://github.com/jonathan-s))

## [0.4.2](https://github.com/jonathan-s/django-sockpuppet/tree/0.4.2) (2020-12-28)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.4.1...0.4.2)

**Implemented enhancements:**

- If lxml and cssselect is installed we use them for better perf. [\#48](https://github.com/jonathan-s/django-sockpuppet/pull/48) ([jonathan-s](https://github.com/jonathan-s))

**Fixed bugs:**

- fix template syntax error [\#66](https://github.com/jonathan-s/django-sockpuppet/pull/66) ([kaozdl](https://github.com/kaozdl))

**Merged pull requests:**

- Proofreading pass [\#65](https://github.com/jonathan-s/django-sockpuppet/pull/65) ([DamnedScholar](https://github.com/DamnedScholar))
- Serializing form data in reflexes [\#40](https://github.com/jonathan-s/django-sockpuppet/pull/40) ([jonathan-s](https://github.com/jonathan-s))

## [0.4.1](https://github.com/jonathan-s/django-sockpuppet/tree/0.4.1) (2020-12-28)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.4.0...0.4.1)

## [0.4.0](https://github.com/jonathan-s/django-sockpuppet/tree/0.4.0) (2020-12-28)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.8...0.4.0)

**Closed issues:**

- Update documentation to refer to Stimulus 2.0 syntax [\#61](https://github.com/jonathan-s/django-sockpuppet/issues/61)
- Introduce an option of using lxml as parser.  [\#46](https://github.com/jonathan-s/django-sockpuppet/issues/46)
- Verify serializing of form data [\#29](https://github.com/jonathan-s/django-sockpuppet/issues/29)

## [0.3.8](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.8) (2020-12-26)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.7...0.3.8)

**Fixed bugs:**

- Fixes to SocketpuppetConsumer for handling dotfiles [\#57](https://github.com/jonathan-s/django-sockpuppet/pull/57) ([mekhami](https://github.com/mekhami))

**Closed issues:**

- When a Reflex with underscore is created with the generator it fails [\#54](https://github.com/jonathan-s/django-sockpuppet/issues/54)

**Merged pull requests:**

- A lightweight alternative to using controllers [\#63](https://github.com/jonathan-s/django-sockpuppet/pull/63) ([jonathan-s](https://github.com/jonathan-s))
- Replace travis with github actions [\#58](https://github.com/jonathan-s/django-sockpuppet/pull/58) ([jonathan-s](https://github.com/jonathan-s))
- Fixing correct path to staticfiles dirs [\#56](https://github.com/jonathan-s/django-sockpuppet/pull/56) ([jonathan-s](https://github.com/jonathan-s))
- Classify name of Class in Python Template \(as this will be done with … [\#55](https://github.com/jonathan-s/django-sockpuppet/pull/55) ([JulianFeinauer](https://github.com/JulianFeinauer))
- Explanation on the architecture to give an overview [\#53](https://github.com/jonathan-s/django-sockpuppet/pull/53) ([jonathan-s](https://github.com/jonathan-s))

## [0.3.7](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.7) (2020-12-24)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.6...0.3.7)

**Merged pull requests:**

- generate package.json as part of inital\_sockpuppet command [\#51](https://github.com/jonathan-s/django-sockpuppet/pull/51) ([kaozdl](https://github.com/kaozdl))

## [0.3.6](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.6) (2020-12-22)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.5...0.3.6)

**Closed issues:**

- Url parameters throws a wrench in the machinery [\#49](https://github.com/jonathan-s/django-sockpuppet/issues/49)

**Merged pull requests:**

- Fix issue with resolving path [\#50](https://github.com/jonathan-s/django-sockpuppet/pull/50) ([jonathan-s](https://github.com/jonathan-s))
- Bump ini from 1.3.5 to 1.3.8 [\#47](https://github.com/jonathan-s/django-sockpuppet/pull/47) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update README.md [\#45](https://github.com/jonathan-s/django-sockpuppet/pull/45) ([zodman](https://github.com/zodman))

## [0.3.5](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.5) (2020-11-29)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.4...0.3.5)

**Closed issues:**

- Figure out how to get python codecoverage working with cypress [\#5](https://github.com/jonathan-s/django-sockpuppet/issues/5)

**Merged pull requests:**

- When using the channel separately to broadcast frontend should listen [\#44](https://github.com/jonathan-s/django-sockpuppet/pull/44) ([jonathan-s](https://github.com/jonathan-s))
- Get coverage from dev server [\#42](https://github.com/jonathan-s/django-sockpuppet/pull/42) ([jonathan-s](https://github.com/jonathan-s))

## [0.3.4](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.4) (2020-11-15)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.3...0.3.4)

**Merged pull requests:**

- Always install the latest stimulus-reflex in CI [\#39](https://github.com/jonathan-s/django-sockpuppet/pull/39) ([jonathan-s](https://github.com/jonathan-s))
- Introduce compatibility with stimulus-reflex 3.4 [\#38](https://github.com/jonathan-s/django-sockpuppet/pull/38) ([jonathan-s](https://github.com/jonathan-s))
- The javascript in static js isn't used, so remove it. [\#37](https://github.com/jonathan-s/django-sockpuppet/pull/37) ([jonathan-s](https://github.com/jonathan-s))
- Sockpuppet not yet compatible with channels 3.0 [\#35](https://github.com/jonathan-s/django-sockpuppet/pull/35) ([jonathan-s](https://github.com/jonathan-s))
- Remove some stray ruby in the docs [\#34](https://github.com/jonathan-s/django-sockpuppet/pull/34) ([jonathan-s](https://github.com/jonathan-s))

## [0.3.3](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.3) (2020-10-31)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.2...0.3.3)

**Closed issues:**

- Javascript modifications [\#1](https://github.com/jonathan-s/django-sockpuppet/issues/1)

## [0.3.2](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.2) (2020-10-18)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.1...0.3.2)

## [0.3.1](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.1) (2020-10-18)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.3.0...0.3.1)

## [0.3.0](https://github.com/jonathan-s/django-sockpuppet/tree/0.3.0) (2020-10-18)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.2.2...0.3.0)

**Implemented enhancements:**

- Subscriptions for other things than sessionid [\#6](https://github.com/jonathan-s/django-sockpuppet/issues/6)

**Closed issues:**

- Trigger handler subscription handler on messages [\#28](https://github.com/jonathan-s/django-sockpuppet/issues/28)
- Update Ruby examples to Django [\#23](https://github.com/jonathan-s/django-sockpuppet/issues/23)

**Merged pull requests:**

- Get django-sockpuppet up to par with SR 3.3.0 [\#30](https://github.com/jonathan-s/django-sockpuppet/pull/30) ([jonathan-s](https://github.com/jonathan-s))
- Better exception handling [\#25](https://github.com/jonathan-s/django-sockpuppet/pull/25) ([jonathan-s](https://github.com/jonathan-s))
- Docs improvement [\#24](https://github.com/jonathan-s/django-sockpuppet/pull/24) ([jonathan-s](https://github.com/jonathan-s))
- Measure how fast a reflex executes in the backend [\#22](https://github.com/jonathan-s/django-sockpuppet/pull/22) ([jonathan-s](https://github.com/jonathan-s))

## [0.2.2](https://github.com/jonathan-s/django-sockpuppet/tree/0.2.2) (2020-05-31)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.2.1...0.2.2)

**Merged pull requests:**

- Html should take the innerhtml to be correct [\#20](https://github.com/jonathan-s/django-sockpuppet/pull/20) ([jonathan-s](https://github.com/jonathan-s))
- Add gitbook yaml [\#19](https://github.com/jonathan-s/django-sockpuppet/pull/19) ([jonathan-s](https://github.com/jonathan-s))
- :pencil: Adds local quickstart reference [\#18](https://github.com/jonathan-s/django-sockpuppet/pull/18) ([jefftriplett](https://github.com/jefftriplett))
- Docs update [\#16](https://github.com/jonathan-s/django-sockpuppet/pull/16) ([jonathan-s](https://github.com/jonathan-s))

## [0.2.1](https://github.com/jonathan-s/django-sockpuppet/tree/0.2.1) (2020-05-08)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.2.0...0.2.1)

## [0.2.0](https://github.com/jonathan-s/django-sockpuppet/tree/0.2.0) (2020-05-03)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/0.1.0...0.2.0)

**Closed issues:**

- The example reflex isn't being picked up by consumer.py on Windows [\#9](https://github.com/jonathan-s/django-sockpuppet/issues/9)

## [0.1.0](https://github.com/jonathan-s/django-sockpuppet/tree/0.1.0) (2020-05-03)

[Full Changelog](https://github.com/jonathan-s/django-sockpuppet/compare/77e740833a7a91e85bbf19f499a187ccf840ceec...0.1.0)

**Closed issues:**

- Setup errors when there are already scripts in place. [\#7](https://github.com/jonathan-s/django-sockpuppet/issues/7)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
