import React, { useState, useEffect, useReducer } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, useParams, useLocation } from 'react-router-dom';
import './light.css';
import { Button, Container, Divider, Dropdown, Form, Grid, Header, Icon, Image, Input, Item, Menu, Message, Segment, Table } from 'semantic-ui-react';
import { statusColor, isAdmin, isInstructor, BasicTable, staticUrl, requester } from './utils.js';
import { NotFound, PleaseLogin } from './Misc.js';
import { AdminMemberInfo, AdminMemberPause, AdminMemberForm, AdminMemberCards, AdminMemberTraining, AdminMemberCertifications } from './AdminMembers.js';
import { AdminMemberTransactions } from './AdminTransactions.js';

const memberSorts = {
	recently_vetted: 'Recently Vetted',
	newest_active: 'Newest Active',
	newest_overall: 'Newest Overall',
	best_looking: 'Best Looking',
	oldest_active: 'Oldest Active',
	oldest_overall: 'Oldest Overall',
};

export function MembersDropdown(props) {
	const { token, name, onChange, value, initial } = props;
	const [response, setResponse] = useState({ results: [] });
	const searchDefault = {seq: 0, q: initial || ''};
	const [search, setSearch] = useState(searchDefault);

	useEffect(() => {
		requester('/search/', 'POST', token, search)
		.then(res => {
			if (!search.seq || res.seq > response.seq) {
				setResponse(res);
			}
		})
		.catch(err => {
			console.log(err);
		});
	}, [search]);

	const options = response.results.map((x, i) => ({
		key: x.member.id,
		value: x.member.id,
		text: x.member.preferred_name + ' ' + x.member.last_name,
		image: { avatar: true, src: x.member.photo_small ? staticUrl + '/' + x.member.photo_small : '/nophoto.png' },
	}));

	return (
		<Dropdown
			clearable
			fluid
			selection
			search
			name={name}
			options={options}
			value={value}
			placeholder='Search for Member'
			onChange={onChange}
			onSearchChange={(e, v) => setSearch({seq: parseInt(e.timeStamp), q: v.searchQuery})}
		/>

	);
};

let searchCache = '';

export function Members(props) {
	const qs = useLocation().search;
	const params = new URLSearchParams(qs);
	const sort = params.get('sort') || 'recently_vetted';

	const [response, setResponse] = useState(false);
	const [numShow, setNumShow] = useState(20);
	const searchDefault = {seq: 0, q: searchCache};
	const [search, setSearch] = useState(searchDefault);
	const { token } = props;

	console.log(sort);

	useEffect(() => {
		setResponse(false);
		searchCache = search.q;
		search.sort = sort;
		requester('/search/', 'POST', token, search)
		.then(res => {
			if (!search.seq || res.seq > response.seq) {
				setResponse(res);
			}
		})
		.catch(err => {
			console.log(err);
		});
	}, [search, sort]);

	return (
		<Container>
			<Header size='large'>Member List</Header>

			<p>Search by name, email, or member ID:</p>

			<Input autoFocus focus icon='search'
				placeholder='Search...'
				value={search.q}
				onChange={(e, v) => setSearch({seq: parseInt(e.timeStamp), q: v.value})}
				aria-label='search products'
				style={{ marginRight: '0.5rem' }}
			/>

			{search.q.length ?
				<Button
					content='Clear'
					onClick={() => setSearch({seq: 0, q: ''})}
				/> : ''
			}

			<p></p>

			<p>
				Sort by{' '}
				{Object.entries(memberSorts).map((x, i) =>
					<>
						<Link to={'/members?sort='+x[0]} replace>{x[1]}</Link>
						{i < Object.keys(memberSorts).length - 1 && ', '}
					</>
				)}.
			</p>

			<Header size='medium'>
				{search.q.length ? 'Search Results' : memberSorts[sort] + ' Members'}
			</Header>

			{sort === 'best_looking' ?
				<center>
					<img className='bean' src='/mr-bean.jpg' />
				</center>
			:
				response ?
					<>
						<Item.Group unstackable divided>
							{response.results.length ?
								response.results.slice(0, numShow).map((x, i) =>
									<Item key={x.member.id} as={Link} to={'/members/'+x.member.id}>
										<div className='list-num'>{i+1}</div>
										<Item.Image size='tiny' src={x.member.photo_small ? staticUrl + '/' + x.member.photo_small : '/nophoto.png'} />
										<Item.Content verticalAlign='top'>
											<Item.Header>
												<Icon name='circle' color={statusColor[x.member.status]} />
												{x.member.preferred_name} {x.member.last_name}
											</Item.Header>
											<Item.Description>Status: {x.member.status || 'Unknown'}</Item.Description>
											<Item.Description>Joined: {x.member.application_date || 'Unknown'}</Item.Description>
											<Item.Description>ID: {x.member.id}</Item.Description>
										</Item.Content>
									</Item>
								)
							:
								<p>No Results</p>
							}
						</Item.Group>

						{numShow !== 100 ?
							<Button
								content='Load More'
								onClick={() => setNumShow(100)}
							/> : ''
						}
					</>
				:
					<p>Loading...</p>
			}

		</Container>
	);
};

let resultCache = {};

export function MemberDetail(props) {
	const { id } = useParams();
	const [result, setResult] = useState(resultCache[id] || false);
	const [refreshCount, refreshResult] = useReducer(x => x + 1, 0);
	const [error, setError] = useState(false);
	const { token, user } = props;

	useEffect(() => {
		requester('/search/'+id+'/', 'GET', token)
		.then(res => {
			setResult(res);
			resultCache[id] = res;
		})
		.catch(err => {
			console.log(err);
			setError(true);
		});
	}, [refreshCount]);

	const member = result.member || false;

	return (
		<Container>
			{!error ?
				member ?
					<div>
						<Header size='large'>{member.preferred_name} {member.last_name}</Header>

						<Grid stackable columns={2}>
							<Grid.Column width={isAdmin(user) ? 8 : 5}>
								<p>
									<Image rounded size='medium' src={member.photo_large ? staticUrl + '/' + member.photo_large : '/nophoto.png'} />
								</p>

								{isAdmin(user) ?
									<AdminMemberInfo result={result} refreshResult={refreshResult} {...props} />
								:
									<React.Fragment>
										<BasicTable>
											<Table.Body>
												<Table.Row>
													<Table.Cell>Status:</Table.Cell>
													<Table.Cell>
														<Icon name='circle' color={statusColor[member.status]} />
														{member.status || 'Unknown'}
													</Table.Cell>
												</Table.Row>
												<Table.Row>
													<Table.Cell>Joined:</Table.Cell>
													<Table.Cell>{member.application_date || 'Unknown'}</Table.Cell>
												</Table.Row>
												<Table.Row>
													<Table.Cell>Public Bio:</Table.Cell>
												</Table.Row>
											</Table.Body>
										</BasicTable>

										<p className='bio-paragraph'>
											{member.public_bio || 'None yet.'}
										</p>
									</React.Fragment>
								}
							</Grid.Column>

							<Grid.Column width={isAdmin(user) ? 8 : 11}>
								{isInstructor(user) && !isAdmin(user) && <Segment padded>
									<AdminMemberTraining result={result} refreshResult={refreshResult} {...props} />
								</Segment>}

								{isAdmin(user) && <Segment padded>
									<AdminMemberForm result={result} refreshResult={refreshResult} {...props} />
								</Segment>}

								{isAdmin(user) && <Segment padded>
									<AdminMemberPause result={result} refreshResult={refreshResult} {...props} />
								</Segment>}
							</Grid.Column>
						</Grid>

						{isAdmin(user) && <Segment padded>
							<AdminMemberCards result={result} refreshResult={refreshResult} {...props} />
						</Segment>}

						{isAdmin(user) && <Segment padded>
							<AdminMemberCertifications result={result} refreshResult={refreshResult} {...props} />
						</Segment>}

						{isAdmin(user) && <Segment padded>
							<AdminMemberTraining result={result} refreshResult={refreshResult} {...props} />
						</Segment>}

						{isAdmin(user) && <Segment padded>
							<AdminMemberTransactions result={result} refreshResult={refreshResult} {...props} />
						</Segment>}

					</div>
				:
					<p>Loading...</p>
			:
				<NotFound />
			}
		</Container>
	);
};

